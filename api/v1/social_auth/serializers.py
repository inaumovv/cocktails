from rest_framework import serializers
from .socials import twitterhelper, google, facebook
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            email = user_data.get('email')
            name = user_data.get('name')
            return register_social_user(email=email, name=name)
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    access_token = serializers.CharField()

    def validate(self, attrs):
        id_token = attrs.get('id_token')
        access_token = attrs.get('access_token')

        user_data = google.Google.validate(id_token, access_token)

        email = user_data.get('email')
        name = user_data.get('name')

        return register_social_user(email=email, name=name)


# class TwitterAuthSerializer(serializers.Serializer):
#     """Handles serialization of twitter related data"""
#     access_token_key = serializers.CharField()
#     access_token_secret = serializers.CharField()
#
#     def validate(self, attrs):
#
#         access_token_key = attrs.get('access_token_key')
#         access_token_secret = attrs.get('access_token_secret')
#
#         user_info = twitterhelper.TwitterAuthTokenVerification.validate_twitter_auth_tokens(
#             access_token_key, access_token_secret)
#
#         try:
#             email = user_info['email']
#             name = user_info['name']
#         except:
#             raise serializers.ValidationError(
#                 'The tokens are invalid or expired. Please login again.'
#             )
#
#         return register_social_user(email=email, name=name)
