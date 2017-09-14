"""Twitter bot that tweets out "Weezy F Baby and the F is for" + a word."""

# Import necessary libraries
import twitter
from wordnik import swagger, WordsApi
import os
import random
import time
from collections import deque

# Authenticate the twitter bot by passing the twitter api keys retrieved from
# environment variables
twitterApi = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                         consumer_secret=os.environ['CONSUMER_SECRET'],
                         access_token_key=os.environ['ACCESS_TOKEN'],
                         access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

# Authenticate wordnik api with api key retrieved from environment variables
apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ['WORDNIK_KEY']
wordnikApi = swagger.ApiClient(apiKey, apiUrl)
wordsAPI = WordsApi.WordsApi(wordnikApi)


def postTweet(startPhrase, endPhrase):
    """Post tweet with given parameters."""
    try:
        status = twitterApi.PostUpdate(startPhrase + ' ' + endPhrase)

    except twitter.error.TwitterError as e:
        print('There was an error: ' + e.message[0]['message'])
        return (False, None)

    else:
        print("%s just posted: %s" % (status.user.name, status.text))
        return (True, endPhrase)


# Define variations of the phrase used in the tweet
phraseVariations = ['Weezy F. Baby and the F is for',
                    'Weezy F., the F is for',
                    'Weezy F. and the F is for',
                    'Weezy F. Baby, the F is for']

# Create a deque that will hold the last 5 trending topics that have been
# tweeted out
lastTrendsTweeted = deque(maxlen=5)

while True:
    # Choose a random variation from the variations defined above
    startingPhrase = random.choice(phraseVariations)

    # Retrieve trending topics from the USA and from the entire world and
    # append the two lists together
    trends = twitterApi.GetTrendsWoeid(23424977)+twitterApi.GetTrendsCurrent()

    # Pick the first trend that starts with f and isn't one of the last 5
    # trends tweeted
    for trend in trends:
        if trend.name not in lastTrendsTweeted and \
          (trend.name.startswith("f") or trend.name.startswith("#f") or
           trend.name.startswith("F") or trend.name.startswith("#F")):

            # Attempt to post the tweet and add the trend to the list of
            # topics tweeted recently
            result = postTweet(startingPhrase, trend.name)

            if result[0]:
                # Note: when a deque with a max length is full, appending
                # on one side will remove the object at the end of the
                # opposite side before adding the new object
                lastTrendsTweeted.appendleft(result[1])
                # Sleep for 2 hours after tweeting
                time.sleep(60*60*2)

            break

    # Pick f or ph randomly with a higher probability of picking f
    firstLetter = random.choices(['f', 'ph'], [30, 1], k=1)[0]
    # Randomly pick a part of speech to search for
    partOfSpeech = random.choices(["noun", "adjective", "verb-transitive"],
                                  [7000, 2000, 400],
                                  k=1)[0]
    # Define totals for each combination of first letter and part of speech.
    # Hardcoded to avoid making two api calls for each word
    if firstLetter == 'f':
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

    # Make api call for a random word
    searchResults = wordsAPI.searchWords(firstLetter,
                                         includePartOfSpeech=partOfSpeech,
                                         caseSensitive=False,
                                         skip=random.randrange(1, total),
                                         limit=1)
    # Get the word from the response
    word = searchResults.searchResults[0].word

    postTweet(startingPhrase, word)

    time.sleep(60*60*2)
