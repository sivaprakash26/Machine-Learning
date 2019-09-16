# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 22:50:01 2019

@author: siva1
"""
import tweepy as tw

consumer_key= 'KeygoesHere'
consumer_secret= 'KeyGoesHere'
access_token= 'KeyGoesHere'
access_token_secret= 'KeyGoesHere'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

# Post a tweet from Python
api.update_status("Look, I'm tweeting from #Python in my #earthanalytics class! @EarthLabCU")
# Your tweet has been posted!

public_tweets = api.home_timeline()
# foreach through all tweets pulled
for tweet in public_tweets:
   # printing the text stored inside the tweet object
   print(tweet.text)

# Define the search term and the date_since date as variables
search_words = "#Apple"
date_since = "2019-01-01"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(5)

# Iterate and print tweets
for tweet in tweets:
    print(tweet.text)
    
new_search = search_words + " -filter:retweets"
new_search


tweets = tw.Cursor(api.search, 
                           q=new_search,
                           lang="en",
                           since=date_since).items(1000)

users_locs = [[tweet.user.screen_name, tweet.user.location, tweet.text] for tweet in tweets]
users_locs

import pandas as pd
tweet_text = pd.DataFrame(data=users_locs, 
                    columns=['user', "location", "Tweet"])
tweet_text

new_search = "climate+change -filter:retweets"

tweets = tw.Cursor(api.search,
                   q=new_search,
                   lang="en",
                   since='2018-04-23').items(1000)

all_tweets = [tweet.text for tweet in tweets]
all_tweets[:5]

user = api.get_user("@CNBCFastMoney")

print("User details:")
print(user.name)
print(user.description)
print(user.location)

print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)
    
alltweets = []	
#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = "CNBCFastMoney",count=200)
#save most recent tweets
alltweets.extend(new_tweets)
#save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1
#keep grabbing tweets until there are no tweets left to grab
while len(new_tweets) > 0:
    print("getting tweets before %s" % (oldest))
    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = "CNBCFastMoney",count=200,max_id=oldest)
    #save most recent tweets
    alltweets.extend(new_tweets)
    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print("...%s tweets downloaded so far" % (len(alltweets)))
#transform the tweepy tweets into a 2D array that will populate the csv	
outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
