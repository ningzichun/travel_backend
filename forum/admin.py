from django.contrib import admin
from forum.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id','time','uid','title','like_num')
 
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id','time','post_id','text','like_num')
 

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)