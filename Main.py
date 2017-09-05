"""Twitter bot that tweets out "Weezy F Baby and the F is for" + a word."""

import twitter
from wordnik import *
import os
import sys
import random
import time

twitterApi = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                         consumer_secret=os.environ['CONSUMER_SECRET'],
                         access_token_key=os.environ['ACCESS_TOKEN'],
                         access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ['WORDNIK_KEY']
wordnikApi = swagger.ApiClient(apiKey, apiUrl)
wordsAPI = WordsApi.WordsApi(wordnikApi)

while True:
    query = random.choices(['f', 'ph'], [30, 1], k=1)[0]
    if query == 'f':
        total = 7586
    else:
        total = 1055
    searchResults = wordsAPI.searchWords(query,
                                         includePartOfSpeech='noun,adjective,\
                                         verb-transitive',
                                         caseSensitive=False,
                                         skip=random.randrange(1, total),
                                         limit=1)

    print(searchResults)
    print(searchResults.totalResults)
    word = searchResults.searchResults[0].word

    try:
        status = twitterApi.PostUpdate('Weezy F. Baby and the F is for' + word)
    except UnicodeDecodeError:
        print("Your message could not be encoded. Perhaps it contains \
        non-ASCII characters?")
        print("Try explicitly specifying the encoding with \
        the --encoding flag")
        sys.exit(2)
    print("%s just posted: %s" % (status.user.name, status.text))

    time.sleep(300)
