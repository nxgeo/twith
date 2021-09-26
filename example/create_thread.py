from twith import OAuth1, Twith, TwithError

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

auth = OAuth1(
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

tt = Twith(auth)

text = ""
# tweet_id = ''

try:
    r = tt.create_thread(text)
    # r = tt.create_thread(text, tweet_id)
except TwithError as e:
    print(e)
else:
    print(r)
