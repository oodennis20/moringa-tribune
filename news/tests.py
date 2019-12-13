from django.test import TestCase
from .models import Editor,tags,Article
import datetime as dt
class EditorTestClass(TestCase):

  def setUp(self):
    self.pyra=Editor(first_name='Pyra',last_name='Myra',email='pyra@gmail.com')

  def test_instance(self):
    self.assertTrue(isinstance(self.pyra,Editor))

  def test_save(self):
    self.pyra.save_editor()
    editors=Editor.objects.all()
    self.assertTrue(len(editors)>0)

class ArticleTestClass(TestCase):
  def setUp(self):
    self.pyra=Editor(first_name='Pyra',last_name='Myra',email='pyra@gmail.com')
    self.pyra.save_editor()


    self.new_tag=tags(name='testing')
    self.new_tag.save()

    # share one to many relationship
    self.new_artcile=Article(title='hacks',post='Hack 20 computer per day',editor=self.pyra)
    self.new_artcile.save()

    #share many to many relationship
    self.new_artcile.tags.add(self.new_tag)

  def tearDown(self):    
    Editor.objects.all().delete()
    tags.objects.all().delete()
    Article.objects.all().delete()

  def test_get_today(self):
    today_news=Article.today_news()
    self.assertTrue(len(today_news)>0)

  def test_get_news_by_date(self):
    test_date='2017-01-10' 
    date=dt.datetime.strptime(test_date,'%Y-%m-%d').date()
    news_by_date=Article.days_news(date)
    self.assertTrue(len(news_by_date)==0)











