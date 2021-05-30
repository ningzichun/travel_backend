from django.db import models
from user.models import User
from django.utils import timezone

class Work(models.Model):
    work_id = models.AutoField(verbose_name='作业号',primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户')
    
    create_time = models.DateTimeField(verbose_name='创建时间',default=timezone.now)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    status = models.SmallIntegerField(
        choices=((0,'未开始'),(100,"排队等待中"),(200,"已生成"),(-1,"生成失败"),(-2,"已过期")),
        default=0,
        verbose_name="状态",
    )
    status_msg = models.CharField(max_length=256,verbose_name='状态描述',null=True)
    result_msg = models.CharField(max_length=256,verbose_name='信息',null=True)

    movie_title = models.CharField(max_length=256,verbose_name='标题',null=True)
    movie_description = models.CharField(max_length=256,verbose_name='影集描述',null=True)
    movie_cover = models.CharField(max_length=256,verbose_name='封面图',null=True)
    tag = models.IntegerField(verbose_name='分类',default=1)
    share_tag = models.BooleanField(verbose_name='分享',default=True)
    like_num = models.IntegerField(verbose_name='赞数',default=0)
    comment_num = models.IntegerField(verbose_name='评论数',default=0)

    class Meta:
        verbose_name = '影集'
        verbose_name_plural = '影集表'
    def __str__(self):
        return "%s: %s"% (self.work_id,self.movie_title)

class WorkComment(models.Model):
    comment_id = models.AutoField(verbose_name='评论号',primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    work = models.ForeignKey(Work, on_delete=models.CASCADE,verbose_name='关联影集')
    text = models.TextField(verbose_name='评论文本')
    time = models.DateTimeField(verbose_name='时间',default=timezone.now)
    like_num = models.IntegerField(verbose_name='赞数',default=0)
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论表'
    def __str__(self):
        return "%s: %s"% (self.comment_id,self.text)
