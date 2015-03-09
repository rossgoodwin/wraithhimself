#!/usr/bin/env python

import tweepy
import json
from time import sleep
import string
import re
import os

N = 361

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

ijFile = open('ij.json', 'r')
ijTokens = json.load(ijFile)
ijFile.close()

# print "SLEEPING 15 MIN..."
# sleep(900)
# print "...DONE SLEEPING"

i = N
for token in ijTokens[N:]:
    candidates = [] # list of result objects
    while not candidates:
        try:
            results = api.search(q=token)

            for r in results:
                # print r.text + "\n"
                if re.match("\.?[@#]?%s([^a-z]|$)"%token,r.text.lower()) is not None:
                    # print "\n\nMATCH FOUND\n\n"
                    candidates.append(r)

            sleep(5)

        except tweepy.TweepError:
            # print "\n\nRATE LIMIT REACHED\n\n"
            # print "Tweep Error"
            sleep(60)
            continue

    api.retweet(candidates[0].id)

    # print "TWEETED WORD " + str(i)
    # print "Tweeted"
    sleep(300)

    i += 1





