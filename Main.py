"""Twitter bot that tweets out "Weezy F Baby and the F is for" + a word."""

import twitter
from wordnik import *
import os
import random
import time
from collections import deque

twitterApi = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                         consumer_secret=os.environ['CONSUMER_SECRET'],
                         access_token_key=os.environ['ACCESS_TOKEN'],
                         access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ['WORDNIK_KEY']
wordnikApi = swagger.ApiClient(apiKey, apiUrl)
wordsAPI = WordsApi.WordsApi(wordnikApi)

phraseVariations = ['Weezy F. Baby and the F is for',
                    'Weezy F., the F is for',
                    'Weezy F. and the F is for',
                    'Weezy F. Baby, the F is for']

lastTrendsTweeted = deque(maxlen=5)

while True:

    startingPhrase = random.choice(phraseVariations)

    trends = twitterApi.GetTrendsWoeid(23424977)+twitterApi.GetTrendsCurrent()
    for trend in trends:
        if trend.name not in lastTrendsTweeted and \
          (trend.name.startswith("f") or trend.name.startswith("#f") or
           trend.name.startswith("F") or trend.name.startswith("#F")):

            try:
                status = twitterApi.PostUpdate(startingPhrase +
                                               ' ' + trend.name)
            except twitter.error.TwitterError as e:
                print('There was an error: ' + e.message[0]['message'])
                break

            print("%s just posted trend: %s" % (status.user.name, status.text))
            lastTrendsTweeted.appendleft(trend.name)

            time.sleep(60*60*3)
            break

    query = random.choices(['f', 'ph'], [30, 1], k=1)[0]

    partOfSpeech = random.choices(["noun", "adjective", "verb-transitive"],
                                  [7000, 2000, 400],
                                  k=1)[0]

    if query == 'f':
        if partOfSpeech == "noun":
            total = 5436
        elif partOfSpeech == "adjective":
            total = 1819
        else:
            total = 333
    else:
        if partOfSpeech == "noun":
            total = 823
        elif partOfSpeech == "adjective":
            total = 215
        else:
            total = 19

    searchResults = wordsAPI.searchWords(query,
                                         includePartOfSpeech=partOfSpeech,
                                         caseSensitive=False,
                                         skip=random.randrange(1, total),
                                         limit=1)

    word = searchResults.searchResults[0].word

    try:
        status = twitterApi.PostUpdate(startingPhrase +
                                       ' ' + trend.name)
    except twitter.error.TwitterError as e:
        print('There was an error:' + e.message[0]['message'])
        continue

    print("%s just posted: %s" % (status.user.name, status.text))

    time.sleep(60*60*3)
