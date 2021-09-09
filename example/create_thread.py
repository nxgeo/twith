from twith import Twith, TwithError

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

tt = Twith(
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

text = ""
# tweet_id = ''

try:
    res = tt.create_thread(text)
    # res = tt.create_thread(text, tweet_id)
except TwithError as e:
    print(e)
else:
    print(res)
