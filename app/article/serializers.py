from rest_framework import serializers
from article import models


class PopArticleReq(serializers.Serializer):
    article_id = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=100)
    )


class ArticleEditReq(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ('title','image','link',)