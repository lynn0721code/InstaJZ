from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView
from Insta.models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 

#HelloWorld is a TemplateView

class HelloWorld(TemplateView): #不用import template，因为已经在settings.py中已经定义
    template_name = 'test.html'

class PostsView(ListView): #ListView 会将所有的posts生成为一个lists传递给index.html,用于里面的for loop显示
    model = Post 
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post 
    template_name = 'post_detail.html' 

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = {'title'}

class PostDeleteView(DeleteView):
    model = Post 
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")
