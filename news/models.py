from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# from django.db.models.signals import post_save
# from django.dispatch import receiver

class tags(models.Model):
  name=models.CharField(max_length=30)

  def __str__(self):
      return self.name

class Article(models.Model):
  title=models.CharField(max_length=60)
  post=HTMLField()
  editor=models.ForeignKey(User,on_delete=models.PROTECT,)
  tags=models.ManyToManyField(tags)
  likes=models.ManyToManyField(User ,related_name='likes', blank=True)
  pub_date=models.DateTimeField(auto_now_add=True)
  articles_image=models.ImageField(upload_to='articles/',blank=True)
  
  @classmethod
  def today_news(cls):
    today=dt.date.today()
    news=cls.objects.filter(pub_date__date=today)
    return news

  @classmethod
  def days_news(cls,date)  :
    news=cls.objects.filter(pub_date__date=date)
    return news

  @classmethod  
  def search_by_article(cls,search_term):
    news=cls.objects.filter(title__icontains=search_term)
    return news

  @classmethod
  def usernews(cls,username):
    newes=cls.objects.filter(editor__current_user__icontains=username)  

    return newes
    
class NewsLetter(models.Model):
  name=models.CharField(max_length=30)
  email=models.EmailField()


class MoringaMerch(models.Model):
  name=models.CharField(max_length=40)  
  description=models.TextField()
  price=models.DecimalField(decimal_places=2,max_digits=20)
  
  def __str__(self):
      return self.name

    





  




  
    



