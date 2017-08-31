"""Twitter bot that tweets out "Weezy F Baby and the F is for" + a word."""

import twitter
import os

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

status = api.PostUpdate('Weezy F. Baby and the F is for Fracking')
