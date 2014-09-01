#! /usr/bin/env python

## code for lexicon matcher component

from TweetPreProcessor import get_tweets

from pytagcloud import make_tags, create_tag_image
from pytagcloud.lang.counter import get_tag_counts


from pylab import *

import os



################# extraction of sentiments #######################################

def getDic():
      ''' returns a dictionary for nrc emotion lexicon '''
      dic  = {}
      f = open('tweet_sentiment_vis/src/lexicon_matcher/lexicon.txt','r')
      tmpstr = f.readline()
      while tmpstr!="":
          liss = []
          words = tmpstr.split()
          if words[2]=='1':
             liss.append(0)
          for i in range(9):
            tmpstr = f.readline()
            words = tmpstr.split()
            if words[2]=='1':
              liss.append(i+1)
          dic[words[0]] = liss
          tmpstr = f.readline()
      return dic

def label_sentiments(Tweets):
       
        dic = getDic()
       
        for tweet in Tweets:
             
             tweetwords = tweet.text.split()
             labels = []
             for tweetword in tweetwords:
                     
                     try: 
                       labels.append(dic[tweetword])
                      
                     except KeyError:
                        pass
                     
             tweet.sentiments = labels
                   
        return     

def remove_repeated_tags(Tweets):
      
          for Tweet in Tweets:
                 new_labels = []
                 for label in Tweet.sentiments:
                        for l in label:
                               if l not in new_labels:
                                      new_labels.append(l)
                 Tweet.sentiments = new_labels
          return                              
###################################################################################################################

def analyze(Tweets):
      ''' input tweets and it will give you analysis at macro level '''
      os.remove('tweet_sentiment_vis/static/images/piechart.png')
      liss = []
      
      for i in range(10):
         liss.append(1)
    
      for Tweet in Tweets:
           
           for l in Tweet.sentiments:
              for t in l:
                 liss[t] += 1
 
      figure(1,figsize=(6,6))
      clf()
      ax = axes([0.1,0.1,0.8,0.8])

      labels = 'anger','anticipation','disgust','fear','joy','sadness','surprise','trust'

      fracs = [liss[0],liss[1],liss[2],liss[3],liss[4],liss[7],liss[8],liss[9]]
      explode = (0,0.05,0,0,0,0,0,0)
      
      pie(fracs,explode=explode,labels=labels)
      

      savefig('tweet_sentiment_vis/static/images/piechart.png')
      return liss



def getStopDic():
       f = open('tweet_sentiment_vis/src/lexicon_matcher/stop_words.txt','r')
   
       line = f.readline()
       dic = {}
       while line!="":
               words = line.split()
               dic[words[0]] = 1
               line = f.readline()
 
       return dic


class Topic:
       resul = '1'
       topic = ""
       freq = 0 

def extract_topics(tweets):
        '''  this will extract topics   '''

        dic2 = {}

        stopdic = getStopDic()

        for tweet in tweets:
                  words = (tweet.text).split()
                  for word in words:
                    try:
                      if stopdic[word] == 1:
                              pass
                    except KeyError:
                     
                      if word!="AT_USER" and word!="URL" and word!="ATUSER" and word!="&amp;" and word!="...":
                        try:
                         dic2[word] = dic2[word] + 1
                        except KeyError:
                           dic2[word] = 1

        ### now let's use this dictionary
        list1 = []
        for k in dic2.keys():
             list1.append([dic2[k],k])

        topics = sorted(list1)
         
        topicslist = []
        for to in topics:
               newone = Topic()
               newone.topic = to[1]
               newone.freq = to[0]
               topicslist.append(newone)

        topicslist.reverse()
        
        su = 0
        for to in topicslist:
            su = su + to.freq

        for to in topicslist:
              val = (to.freq)*100.0/su
              if val > 0.3:
                  to.resul = '1'
              elif val > 0.2 and val < 0.3:
                  to.resul = '2'
              elif val > 0.1 and val < 0.4:
                  to.resul = '3'
              elif val < 0.1:
                 to.resul = '5'
       
        return topicslist

import re


def get_string(topics):
        avoidlist = ["http","http...","htt.."]
        s =""
        for t in topics:
          for i in range(t.freq):
            if t.resul=='1' and t.resul=='2':
             if t.topic not in avoidlist:
              (t.topic).replace(".","")
              t.topic = re.sub('[\s]+', ' ', t.topic)
              s = s + t.topic + " "
        return s



def match():
     ''' returns labeled tweets '''
     
     Tweets  = get_tweets()

     label_sentiments(Tweets)
     
     ana = analyze(Tweets)
     

     topics = extract_topics(Tweets)
  
     remove_repeated_tags(Tweets)

     s = get_string(topics)

     tags = make_tags(get_tag_counts(s))

    
     create_tag_image(tags,'tweet_sentiment_vis/static/images/tagcloud.png',size=(1000,500))     


     return [Tweets,ana,topics]



