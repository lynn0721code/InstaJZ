from annoying.decorators import ajax_request
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView
from Insta.models import Post, Like, InstaUser, UserConnection, Comment
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
    #login_url = "login"
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return

        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)    

class PostDetailView(DetailView):
    model = Post 
    template_name = 'post_detail.html' 

class UserDetailView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    login_url = 'login' 


class EditProfile(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'

#CreateView, UpdateView 和 DeleteView都是基于form 来完成的
#PostCreateView 就是处理Post里面所有的field, PostUpdateView处理的就是Post里面所有的title
#PostDeleteView 就是针对整个表格。
class PostCreateView(LoginRequiredMixin, CreateView): #只有log in 过后才能create, 因为
    model = Post                                      #加入了 LoginRequiredMixin
    template_name = 'post_create.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }


@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }


@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }