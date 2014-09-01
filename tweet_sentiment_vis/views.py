from django.http import HttpResponse

from django.shortcuts import render

from src.twitter_handler import Fetcher
from src.lexicon_matcher import Matcher

def index(request):
      return render(request,'index.html',{})



def emotion(request):
     if 'q' in request.GET.keys():
        q = request.GET['q']
        tweetlist = Fetcher.fetch(q)
        ans = Matcher.match()
        sentiments = ans[0]
        ana = ans[1]
        topics = ans[2]
        
        return render(request,'emotion.html',{'tweetlist':tweetlist,'q':q,'sentiments':sentiments,'ana':ana,'topics':topics})

     else:
       return HttpResponse("Error: Key not Valid")

       
