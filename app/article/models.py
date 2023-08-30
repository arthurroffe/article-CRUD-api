from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    post_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'articles'


class PopularArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'popular_articles'