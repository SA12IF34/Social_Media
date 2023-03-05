from rest_framework import serializers
from .models import *



class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):

    file = serializers.FileField(required=False)

    class Meta:
        model = Post
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'