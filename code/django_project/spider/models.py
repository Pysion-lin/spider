from  django.db import models

# Create your models here.

class BigTag(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    btag = models.CharField(max_length=31, unique=True, null=False)

# 一对多
class SmallTag(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    stag = models.CharField(max_length=31, unique=True, null=False)
    btag = models.ForeignKey(BigTag,on_delete=True)

class Book(models.Model):
    '''
    {
      "author": str,
      "publisher": str,
      "producer": str,
      "original_title": str,
      "translator": str,
      "publish_time": datetime,
      "page_number": int,
      "price": float,
      "pack": str,
      "series": str,
      "isbn": str/long int,
      "subtitle": str,
      "title": str,
      "rating_num": float,
      "book_summary": text,
      "author_summary": text
    }
    '''
    __tablename__ = 'book'

    author = models.CharField(max_length=63, null=False, db_index=True)
    publisher = models.CharField(max_length=63, null=True, db_index=True)
    producer = models.CharField(max_length=63, null=True)
    original_title = models.CharField(max_length=63, null=True)
    translator = models.CharField(max_length=63, null=True)
    publish_time = models.DateTimeField(null=False)
    page_number = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    pack = models.CharField(max_length=63, null=True)
    series = models.CharField(max_length=63, null=True)
    isbn = models.CharField(max_length=20, unique=True, primary_key=True)
    subtitle = models.CharField(max_length=63, null=True)
    title = models.CharField(max_length=63, null=False, db_index=True)
    rating_num = models.FloatField(null=False)
    book_summary = models.TextField(null=False)
    author_summary = models.TextField(null=False)

    stag = models.ManyToManyField(SmallTag)    # 多对多关系