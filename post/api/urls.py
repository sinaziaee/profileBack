from django.urls import path
from post.api import views

urlpatterns = [
    path('post/', views.Posts.as_view()),
    path('post/all/', views.get_all_posts),
]
