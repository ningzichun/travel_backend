from django.db import models
from user.models import User
from django.utils import timezone

class Work(models.Model):
    work_id = models.AutoField(verbose_name='作业号',primary_key=True)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户')
    
    create_time = models.DateTimeField(verbose_name='创建时间',default=timezone.now)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    status = models.SmallIntegerField(
        choices=((0,'未开始'),(100,"排队等待中"),(200,"正在生成"),(300,"已生成"),(-100,"生成失败"),(-200,"已过期")),
        default=0,
        verbose_name="状态",
    )
    status_msg = models.CharField(max_length=256,verbose_name='状态描述',null=True)
    result_msg = models.CharField(max_length=256,verbose_name='信息',null=True)

    movie_title = models.CharField(max_length=256,verbose_name='标题',null=True)
    movie_description = models.CharField(max_length=256,verbose_name='影集描述',null=True)
    movie_cover = models.CharField(max_length=256,verbose_name='封面图',null=True)
    class Meta:
        verbose_name = '影集'
        verbose_name_plural = '影集表'
    def __str__(self):
        return "%s: %s"% (self.post_id,self.title)