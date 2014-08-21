#! /usr/bin/env python

### tweet pre-processor

from tweet_sentiment_vis.models import TweetObject
import re

# class Tweet is an object for a processed tweet
class Tweet:
         text =""
         user =""
         date =""
         sentiments = []



def ravikirajprocessing(tweet_text):
        ''' this does basic text based processing'''
        #Convert to lower case
        tweet_text = tweet_text.lower()
        #Convert www.* or https?://* to URL
        tweet_text = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet_text)
        #Convert @username to AT_USER
        tweet_text = re.sub('@[^\s]+','AT_USER',tweet_text)
        
        puncs = ['!',',','(',')','?','.','_','/',';',':','&','-','~','`','|',"'",'"','+','=','[',']','<','>','*','^','$']
        
        news = ""
        for c in tweet_text:
             if c in puncs:
               pass
             else:
               news = news + c
        tweet_text = news                    

        
        #Remove additional white spaces
        tweet_text = re.sub('[\s]+', ' ', tweet_text)
        #Replace #word with word
        tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet_text)
        tweet_text = re.sub(r'([^\s]*)([.])+([^\s]*)', r'\1', tweet_text)
        #trim
        tweet_text = tweet_text.strip('\'"')
        return tweet_text
        #end




def process(Tweets):
      ''' main tweet pre processor '''

      ProcessedTweets = []
      for tweet in Tweets:
               t = Tweet()
               t.text = ravikirajprocessing(tweet.text)
               t.user = tweet.user
               t.date = tweet.date
               t.sentiments = []
               ProcessedTweets.append(t)
      return ProcessedTweets
             


def get_tweets():
     ''' flushes all the tweets from the database after processing '''
     

     Tweets = TweetObject.objects.all()

     ProcessedTweets = process(Tweets)     
 
    
     return ProcessedTweets


