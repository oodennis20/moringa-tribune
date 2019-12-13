from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
import datetime as dt
from .models import Article

def convert_dates(dates):
  day_number=dt.date.weekday(dates)

  days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

  day=days[day_number]
  return day

def news_of_day(request):
  date=dt.date.today()
  news=Article.today_news()
    
  return render(request,'today.html',{"date":date,"news":news})  


def past_days_news(request,past_date):

  try:
    date=dt.datetime.strptime(past_date,'%Y-%m-%d').date()
  except ValueError:
    raise Http404()
    # assert False

  if date == dt.date.today():
    return redirect(news_of_day)        

  news=Article.days_news(date)
  
  return render(request,'news.html',{"date":date,"news":news})  

def search_results(request):  
    if 'article' in request.GET and request.GET["article"]:
      search_term=request.GET.get('article')
      searched_results=Article.search_by_article(search_term)
    if searched_results:
    
      message=f"{search_term}"

      return render(request,'search.html',{"message":message,"articles":searched_results})

    else:
      message="You haven't searched for any term"  
      return render(request, 'search.html',{"message":message})

def article(request,article_id):
  try:
    article=Article.objects.get(id=article_id)

  except DoesNotExist:
    raise Http404()

  return render(request,'article.html',{"article":article}) 


  