from rest_framework import serializers
from post.models import *


class PostSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
