"""Twitter bot that tweets out "Weezy F Baby and the F is for" + a word."""

import twitter
import os
import sys

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

try:
        status = api.PostUpdate('Weezy F. Baby and the F is for Foodie')
except UnicodeDecodeError:
        print("Your message could not be encoded. Perhaps it contains \
        non-ASCII characters?")
        print("Try explicitly specifying the encoding with \
        the --encoding flag")
        sys.exit(2)
print("%s just posted: %s" % (status.user.name, status.text))
