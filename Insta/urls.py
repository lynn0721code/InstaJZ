"""InstaJZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from Insta.views import (HelloWorld, PostsView, PostDetailView, 
                        addLike, PostCreateView, PostUpdateView, PostDeleteView,
                        UserDetailView, EditProfile, toggleFollow, addComment) 

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloWorld'), #当输入是空的时候返回hello world
    path('', PostsView.as_view(), name = 'posts'),#当传递进来的路径是posts的时候，我们会用PostsView.as_view()这个函数
    path('post/<int:pk>', PostDetailView.as_view(), name = 'post_detail'), #a key will be provided with the post and use it as primary key to render it.
    path('post/new/', PostCreateView.as_view(), name = 'make_post'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name = 'post_update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name = 'post_delete'),
    path('like', addLike, name='addLike'),
    path('user/<int:pk>', UserDetailView.as_view(), name = 'user_detail'),
    path('edit_profile/<int:pk>/', EditProfile.as_view(), name = 'edit_profile'),
    path('togglefollow', toggleFollow, name = 'togglefollow'),
    path('comment', addComment, name='addComment'),

]