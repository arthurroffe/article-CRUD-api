from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiResponse, extend_schema
from article import models, serializers
from core.functions import ApiRes
import os


class PopularArticleViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=['popular article'],
            summary='popular articles list'
    )
    def list(self, request):
        query_pop = models.PopularArticle.objects.all()
        result = []

        for i in query_pop:
            query_article = models.Article.objects.get(id=i.article_id)
            article_dic = {
                'id': i.id,
                'article_id': query_article.id,
                'title': query_article.title,
                'date': query_article.post_date.strftime('%Y-%m-%d'),
                'article_link': f"{os.environ.get('ARTICLE_LINK')}{query_article.link}",
                'image_link': f"{os.environ.get('IMAGE_LINK')}{query_article.image}"
            }
            result.append(article_dic)

        return ApiRes().set_success_msg().generate(status_code=status.HTTP_200_OK, return_data=result)
    
    @extend_schema(
            tags=['popular article'],
            summary='add article to popular table',
            request=serializers.PopArticleReq
    )
    def create(self, request):
        serializer = serializers.PopArticleReq(data=request.data)
        if serializer.is_valid() is False:
            return ApiRes().set_parameters_err().generate(status_code=status.HTTP_400_BAD_REQUEST)

        article_id_list = serializer.validated_data.get('article_id')

        if len(article_id_list) == 0:
            return ApiRes().set_parameters_err().generate(status_code=status.HTTP_400_BAD_REQUEST)
        for i in article_id_list:
            with transaction.atomic():
                query = models.PopularArticle.objects.update_or_create(article_id=i)

        return ApiRes().set_success_msg().generate(status_code=status.HTTP_200_OK, return_data=article_id_list)
    
    @extend_schema(
            tags=['popular article'],
            summary='delete article from popular table',
    )
    def destroy(self, request, pk: int):
        query = models.PopularArticle.objects.filter(id=pk)
        query.delete()

        return ApiRes().set_success_msg().generate(status_code=status.HTTP_200_OK)


class ArticleViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleEditReq