from django.db import models

# Create your models here.


class News(models.Model):
    source = models.CharField(max_length=255)
    type_news = models.CharField(max_length=255)
    title = models.TextField()
    article = models.TextField(null=True)
    img_article_url = models.CharField(max_length=255, null=True)
    title_url = models.CharField(max_length=255, null=True)
    url = models.TextField(null=True)
    author = models.CharField(max_length=255, null=True)
    author_link = models.CharField(max_length=255, null=True)
    datetime = models.DateTimeField(null=True)


