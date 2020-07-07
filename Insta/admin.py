from django.contrib import admin

from Insta.models import Post, InstaUser, Like, UserConnection, Comment  
# Register your models here.

admin.site.register(Post) 
admin.site.register(InstaUser) #往admin这个网站上面register这个自定义的user
admin.site.register(Like)
admin.site.register(UserConnection)
admin.site.register(Comment)
