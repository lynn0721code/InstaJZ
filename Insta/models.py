from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse 
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Post(models.Model): 
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts', #image 都储存在post里面
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True,
    )
    #if someone create a post, it will redirect to get_absolute_url
    def get_absolute_url(self):
        return reverse("post_detail", args = [str(self.id)])

class InstaUser(AbstractUser): #在继承Django中自带的AbstractUser后再自己定义一个profile picture
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles', 
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null = True,
    )