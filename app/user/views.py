from django.shortcuts import render
from rest_framework.permissions import AllowAny  # for Test
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from user.serializers import CreateToken, RenewTokenRes, RenewToken
from core.functions import ApiRes
from django.db import transaction
# Create your views here.


class TokenView(TokenViewBase):
    # permission_classes = [AllowAny]

    @extend_schema(tags=['Auth'],
                   summary='Create token (Sign in)',
                   request=CreateToken,
                   responses={200: CreateToken,
                              401: OpenApiResponse(description="{'error':{'code':'code','message':'message'}}")})
    def post(self, request, *args, **kwargs):
        self._serializer_class = 'user.serializers.CreateTokenExtend'
        return super().post(request, *args, **kwargs)

    @extend_schema(tags=['Auth'],
                   summary='Renew token',
                   request=RenewToken,
                   responses={200: RenewTokenRes,
                              401: OpenApiResponse(description='RefreshToken is incorrect')})
    def put(self, request, *args, **kwargs):
        self._serializer_class = 'user.serializers.RenewToken'
        return super().post(request, *args, **kwargs)

