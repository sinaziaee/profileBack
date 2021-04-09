import json
import base64
import datetime
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from post.models import *
from post.api.serializers import *
from django.db.models import Q
from django.core.files.base import ContentFile


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_posts(request):
    all_events = Post.objects.all()
    serializer = PostSerializer(all_events, many=True)
    data = json.loads(json.dumps(serializer.data))
    for x in data:
        user = Account.objects.get(user_id=x['sender'])
        x['sender'] = user.first_name + ' ' + user.last_name
        print(x)
    return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class Posts(APIView):
    def get(self, args):
        try:
            post_id = self.request.query_params.get('post_id', None)
            # print(post_id)
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response("ERROR: Post not found!",
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        data = json.loads(json.dumps(serializer.data))
        user_id = self.request.user.user_id

        if post.sender.user_id == user_id:
            data['can_delete'] = True

        data['sender'] = post.sender.first_name + ' ' + post.sender.last_name

        if post is not None:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("post: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):
        print(30*'*')
        print(self.request.data)
        try:
            user_id = self.request.user.user_id
            user = Account.objects.get(user_id=user_id)
            request_body = self.request.data
            post = Post()
            post.title = request_body['title']
            post.description = request_body['description']
            post.sender = user
            post.save()
            serializer = PostSerializer(post)
            if len(post.title) != 0 and len(post.description) != 0:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

    def put(self, arg):
        post_id = self.request.query_params.get('post_id', None)
        data = self.request.data
        if post_id is not None:
            try:
                post = Post.objects.get(post_id=post_id)
                user_id = post.sender.user_id
                user = Account.objects.get(user_id=user_id)
                data['sender'] = user.user_id
                data['dateTime'] = datetime.datetime.now()
            except Post.DoesNotExist:
                post = None
            if post is None:
                return Response(f"post_id={post_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(post, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"{serializer.errors}, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("post_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, arg):
        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            try:
                post = Post.objects.get(post_id=post_id)
            except Post.DoesNotExist:
                post = None
            if post is None:
                return Response(f"post_id={post_id}, NOT FOUND", status=status.HTTP_404_NOT_FOUND)
            post.delete()
            return Response(f"post_id={post_id}, DELETED", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("post_id: None, BAD REQUEST ", status=status.HTTP_400_BAD_REQUEST)
