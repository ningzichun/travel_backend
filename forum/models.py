from django.db import models
from user.models import User
from django.utils import timezone

class Post(models.Model):
    post_id = models.AutoField(verbose_name='文章号',primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    title = models.TextField(verbose_name='文章标题')
    post_type = models.SmallIntegerField(verbose_name='类型',null=True)
    cover = models.TextField(verbose_name='封面',null=True)
    text = models.TextField(verbose_name='正文')
    reference = models.TextField(verbose_name='引用',null=True)
    time = models.DateTimeField(verbose_name='时间',default=timezone.now)
    like_num = models.IntegerField(verbose_name='赞数',default=0)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章表'
    def __str__(self):
        return "%s: %s"% (self.post_id,self.title)

class Comment(models.Model):
    comment_id = models.AutoField(verbose_name='评论号',primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='关联文章')
    text = models.TextField(verbose_name='评论文本')
    time = models.DateTimeField(verbose_name='时间',default=timezone.now)
    like_num = models.IntegerField(verbose_name='赞数',default=0)
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论表'
    def __str__(self):
        return "%s: %s"% (self.comment_id,self.text)
