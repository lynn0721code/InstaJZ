from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse 
from django.contrib.auth.models import AbstractUser
# Create your models here.

class InstaUser(AbstractUser): #在继承Django中自带的AbstractUser后再自己定义一个profile picture
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles', 
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True,
    )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse('user_detail', args = [str(self.id)])

    def __str__(self):
        return self.username

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Post(models.Model): 
    author = models.ForeignKey( #Post也应该是一个foreign key，因为其应是指向某一个发这个post的用户
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'my_posts' #当我处于当前用户时，我可以通过my_posts来找到我发过的posts.
    )
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts', #image 都储存在post里面
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True,
    )
    def get_like_count(self):
        return self.likes.count()

    #if someone create a post, it will redirect to get_absolute_url
    def get_absolute_url(self):
        return reverse("post_detail", args = [str(self.id)])



class Like(models.Model):
    #这个like model应该告诉我们哪一个用户喜欢哪一个post
    #因此这个model应该是一个关系型model,其应该联系起Post和InstaUser之间的关系
    #Foreignkey 表示这个post并不是哪一个具体的类型，是一个外键，指向post这个model的一个key.
    #并且当post被删除时，Like这个关系也会被删除： on_delete = models.CASCADE
    #
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name='likes')
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'likes'
    )
    #这个like model里面定义了两个fields: post 和 user， 且他们都是外键，他们指向别的model: Post, InstaUser
    #而这个 “likes” 可以帮助在当前外键下找到作用于自己的Like这个关系，比如在某一篇Post下，通过'likes'便可以找到所有对
    #这篇Post点赞的user. 在User上反之便可找到所有自己点过的likes.

    class Meta:
        unique_together = ("post", "user")
        #一个user只可以给一篇post点一个赞
        #即同样的user和post只能出现一次
    
    def __str__(self):
            return 'Like: ' + self.user.username + ' likes ' + self.post.title


# class Comment(models.Model):
#     post = models.ForeignKey()
#     user = models.ForeignKey()
#     comment = models.CharField(max_length = 100)
#     posted_on = models.DateTimeField(auto_now_add = True, editable = False)

#     def __str__(self):
#         return self.comment