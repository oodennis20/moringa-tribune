from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Article,NewsLetter
from .forms import NewsLetterForm,NewsArticleForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
def convert_dates(dates):
  day_number=dt.date.weekday(dates)

  days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

  day=days[day_number]
  return day

def news_of_day(request):
  date=dt.date.today()
  news=Article.today_news()

  if request.method=='POST':
    form=NewsLetterForm(request.POST)
    if form.is_valid():
      name=form.cleaned_data['name']
      email=form.cleaned_data['email']
      recipient=NewsLetter(name=name,email=email)
      recipient.save()
      send_welcome_email(name,email)
      
      HttpResponseRedirect('news_of_day')

  else:
    form=NewsLetterForm()    

  return render(request,'today.html',{"date":date,"news":news,"subform":form})  


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

@login_required(login_url='/accounts/login/')
def article(request,article_id):
  try:
    article=Article.objects.get(id=article_id)

  except DoesNotExist:
    raise Http404()  
  return render(request,'article.html',{"article":article}) 

@login_required(login_url='/accounts/login/')
def new_article(request):
  current_user=request.user
  if request.method=='POST':
    form=NewsArticleForm(request.POST, request.FILES)
    if form.is_valid():
      article=form.save(commit=False)
      article.editor=current_user
      article.save()

    return redirect('newsToday')  

  else:
    form=NewsArticleForm()

  return render(request, 'new_article.html',{"form":form})  
  
def logout_request(request):
  logout(request)
  return redirect('newsToday')

def profile(request):
  title="Profile"
  current_user=request.user
  usernews=Article.usernews(current_user)

  return render(request,'profile.html',{"title":title,"news":usernews})

# class PostLikeRedirect(RedirectView):
#   def get_redirect_url(self,*args, **kwargs):
#     slug=self.kwargs.get("slug")
#     post=get_object_or_404(Article, slug=slug)  
#     url_=post.get_absolute_url()
#     user=self.request.user
#     post.likes.add(user)
#     return url_

def like_post(request):
  post=get_object_or_404(Article, id=request.POST.get('post_id'))  
  post.likes.add(request.user)      
  return redirect('newsToday')



  