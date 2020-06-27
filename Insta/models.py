from django.db import models
from imagekit.models import ProcessedImageField
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