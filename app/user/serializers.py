from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from core import models
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import User

#login
class CreateTokenExtend(TokenObtainSerializer):
    '''
    This class is modified based on rest_framework_simplejwt.serializers.TokenObtainPairSerializer
    djangorestframework-simplejwt = "==5.2.0"
    '''
    token_class = RefreshToken

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['user_id'] = user.id  # type:ignore
        # token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh_token: RefreshToken = self.get_token(self.user)
        access_token: AccessToken = refresh_token.access_token
        data['accessToken'] = str(access_token)
        # data['accessTokenExp'] = access_token.payload.get('exp')
        data['refreshToken'] = str(refresh_token)
        # data['refreshTokenExp'] = refresh_token.payload.get('exp')

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)  # type: ignore
        return data


class CreateToken(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    accessToken = serializers.CharField(read_only=True)
    refreshToken = serializers.CharField(read_only=True)


class RenewTokenReq(serializers.Serializer):
    # This class is modified based on rest_framework_simplejwt.serializers.TokenRefreshSerializer
    # djangorestframework-simplejwt = "==5.2.0"

    refreshToken = serializers.CharField(write_only=True, required=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh_token = self.token_class(attrs["refreshToken"])
        access_token = refresh_token.access_token

        data = {}
        data['accessToken'] = str(access_token)
        # data['accessTokenExp'] = access_token.payload.get('exp')

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh_token.blacklist()
                except AttributeError:
                    pass

        refresh_token.set_jti()
        refresh_token.set_exp()
        refresh_token.set_iat()

        data["refreshToken"] = str(refresh_token)
        # data['refreshTokenExp'] = refresh_token.payload.get('exp')

        return data


class RenewTokenRes(serializers.Serializer):
    accessToken = serializers.CharField(read_only=True)
    # refreshToken = serializers.CharField(read_only=True)
    # accessTokenExp = serializers.IntegerField(read_only=True)


class RenewToken(RenewTokenRes, RenewTokenReq):
    pass

