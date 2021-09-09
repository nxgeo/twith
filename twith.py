from textwrap import wrap
from requests_oauthlib import OAuth1Session


class TwithError(Exception):
    pass


class Twith:
    """Turn long text into a thread on Twitter."""
    def __init__(
            self,
            consumer_key: str,
            consumer_secret: str,
            access_token: str,
            access_token_secret: str
    ):
        self._auth_session = OAuth1Session(
            consumer_key, consumer_secret,
            access_token, access_token_secret
        )

    def _request(
            self, method, endpoint,
            data=None
    ):
        response = self._auth_session.request(
            method, 'https://api.twitter.com/1.1/'+endpoint,
            data=data
        )

        if response.status_code != 200:
            raise TwithError(response.json())

        return response.json()

    def _verify_credentials(self) -> dict:
        return self._request(
            'GET', 'account/verify_credentials.json'
        )

    def _get_status(self, status_id: str) -> dict:
        return self._request(
            'GET', f'statuses/show/{status_id}.json'
        )

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
            status_author = self._get_status(
                in_reply_to_status_id)['user']['screen_name']
            user_context = self._verify_credentials()['screen_name']
            if status_author != user_context:
                text = f'@{status_author} {text}'

        status_max_length = 280

        if len(text) <= status_max_length:
            raise TwithError('The text is too short.')

        if add_cont:
            indicator = ' ({})'.format('cont.')
            status_max_length -= len(indicator)

        statuses = wrap(text, status_max_length)
        statuses_last_index = len(statuses) - 1

        tweets = []
        tweet_id = in_reply_to_status_id

        for i, status in enumerate(statuses):
            if add_cont and i != statuses_last_index:
                status += indicator
            tweet = self._update_status(status, tweet_id)
            tweets.append(tweet)
            if i != statuses_last_index:
                tweet_id = tweet['id_str']

        return tweets