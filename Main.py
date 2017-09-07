"""Twitter bot that tweets out "Weezy F Baby and the F is for" + a word."""

import twitter
from wordnik import *
import os
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

phraseVariations = ['Weezy F. Baby and the F is for',
                    'Weezy F., the F is for',
                    'Weezy F. and the F is for',
                    'Weezy F. Baby, the F is for']

lastTrendTweeted = ''

while True:

    startingPhrase = random.choice(phraseVariations)

    postedTrend = False
    trends = twitterApi.GetTrendsCurrent()+twitterApi.GetTrendsWoeid(23424977)
    for trend in trends:
        if trend.name != lastTrendTweeted and (trend.name.startswith("f") or
           trend.name.startswith("#f") or trend.name.startswith("F") or
           trend.name.startswith("#F")):

            status = twitterApi.PostUpdate(startingPhrase + ' ' + trend.name)

            print("%s just posted: %s" % (status.user.name, status.text))
            postedTrend = True
            lastTrendTweeted = trend.name
            time.sleep(60*60*6)
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

    status = twitterApi.PostUpdate(startingPhrase + ' ' + word)
    print("%s just posted: %s" % (status.user.name, status.text))

    time.sleep(60*60*3)
