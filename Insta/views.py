from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView
from Insta.models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 

from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.forms import CustomUserCreationForm

#HelloWorld is a TemplateView

class HelloWorld(TemplateView): #不用import template，因为已经在settings.py中已经定义
    template_name = 'test.html'

class PostsView(ListView): #ListView 会将所有的posts生成为一个lists传递给index.html,用于里面的for loop显示
    model = Post 
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post 
    template_name = 'post_detail.html' 

#CreateView, UpdateView 和 DeleteView都是基于form 来完成的
#PostCreateView 就是处理Post里面所有的field, PostUpdateView处理的就是Post里面所有的title
#PostDeleteView 就是针对整个表格。
class PostCreateView(LoginRequiredMixin, CreateView): #只有log in 过后才能create, 因为
    model = Post                                      #加入了 LoginRequiredMixin
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = {'title'}

class PostDeleteView(DeleteView):
    model = Post 
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html' #通过这个url来访问
    success_url = reverse_lazy("login") #signup成功过后跳转到什么页面