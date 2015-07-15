#!/usr/bin/env python

import tweepy
import json
from time import sleep
import string
import re
import os

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

# Check status
statusFile = open('status.txt', 'r')
n = int(statusFile.read().strip())
statusFile.close()

for token in ijTokens[n:]:
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

    n += 1

    with open('status.txt', 'w') as outfile:
        outfile.write(str(n))

    # print "TWEETED WORD " + str(i)
    # print "Tweeted"
    sleep(120)

    





