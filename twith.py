from textwrap import wrap

from requests import Session
from requests_oauthlib import OAuth1


class TwithError(Exception):
    pass


class Twith:
    """Turn long text into a thread on Twitter."""
    API_URL = 'https://api.twitter.com/1.1/'

    def __init__(self, auth: OAuth1) -> None:
        self._session = Session()
        self._session.auth = auth

    def _request(self, method, endpoint, data=None):
        try:
            response = self._session.request(
                method, Twith.API_URL+endpoint, data=data
            )
        finally:
            self._session.close()

        if response.status_code != 200:
            raise TwithError(response.json()['errors'])

        return response.json()

    def _get_user(self) -> str:
        r = self._request(
            'GET', 'account/verify_credentials.json'
        )

        return r['screen_name']

    def _get_author(self, status_id: str) -> str:
        r = self._request(
            'GET', f'statuses/show/{status_id}.json'
        )

        return r['user']['screen_name']

    def _update_status(
            self,
            status: str,
            in_reply_to_status_id: str = None
    ) -> dict:
        return self._request(
            'POST', 'statuses/update.json',
            {
                'status': status,
                'in_reply_to_status_id': in_reply_to_status_id
            }
        )

    def create_thread(
            self,
            text: str,
            in_reply_to_status_id: str = None,
            add_cont: bool = True
    ) -> list:
        if in_reply_to_status_id is not None:
            author = self._get_author(in_reply_to_status_id)
            user = self._get_user()
            if author != user:
                text = f'@{author} {text}'
            del author, user

        status_max_length = 280

        if len(text) <= status_max_length:
            raise TwithError('The text is too short.')

        if add_cont:
            indicator = ' ({})'.format('cont.')
            status_max_length -= len(indicator)

        statuses = wrap(text, status_max_length)
        statuses_last_index = len(statuses) - 1

        tweet_id = in_reply_to_status_id
        tweets = []

        for i, status in enumerate(statuses):
            if add_cont and i != statuses_last_index:
                status += indicator
            tweet = self._update_status(status, tweet_id)
            if i != statuses_last_index:
                tweet_id = tweet['id_str']
            tweets.append(tweet)

        return tweets
