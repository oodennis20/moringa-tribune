from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Article,NewsLetter,MoringaMerch
from .forms import NewsLetterForm,NewsArticleForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .serializer import MerchSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsAdminReadOnly

def convert_dates(dates):
  day_number=dt.date.weekday(dates)

  days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

  day=days[day_number]
  return day

def news_of_day(request):
  date=dt.date.today()
  news=Article.today_news()  
  form=NewsLetterForm()                                    
  return render(request,'today.html',{"date":date,"news":news,"subform":form})  

def newsletter(request):
  name=request.POST.get('name')
  email=request.POST.get('email')
  recipient=NewsLetter(name=name,email=email)
  recipient.save()
  send_welcome_email(name,email)
  data={'success': 'You have been succesfully added to the mail list'}
  return JsonResponse(data)
  
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

class MerchList(APIView):
  permission_classes=(IsAdminReadOnly,)  
  def get(self, request,format=None):
    all_merch=MoringaMerch.objects.all()
    serializers=MerchSerializer(all_merch,many=True)
    return Response(serializers.data)

  def post(self, request,format=None):
    serializers=MerchSerializer(data=request.data)
    if serializers.is_valid():          
      serializers.save()
      return Response(serializers.data,status=status.HTTP_201_CREATED)
    
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class merchdescription(APIView):
  permission_classes=(IsAdminReadOnly,)
  def get_merch(self, pk):
    try:
      return MoringaMerch.objects.get(pk=pk)
    except MoringaMerch.DoesNotExist:
      return Http404

  def get(self, request, pk, format=None):
    merch = self.get_merch(pk)
    serializers=MerchSerializer(merch)
    return Response(serializers.data)

  def put(self,request,pk,format=None):
    merch=self.get_merch(pk)
    serializers=MerchSerializer(merch,request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data)
    else:
      return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)  

  def delete(self,request,pk,formart=None):
    merch=self.get_merch(pk)
    merch.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    




    



  