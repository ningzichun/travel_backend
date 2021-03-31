from django.db import models
from user.models import User
from django.utils import timezone



class Collection(models.Model):
    collection_id = models.AutoField(verbose_name='图片集号',primary_key=True),
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='所属用户'),
    time = models.DateTimeField(verbose_name='时间',default=timezone.now)
    class Meta:
        verbose_name = '图片集'
        verbose_name_plural = '图片集表'
    def __str__(self):
        return "%s"% (self.collection_id)

class Photo(models.Model):
    photo_id = models.AutoField(verbose_name='图片号',primary_key=True),
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE,verbose_name='所属图片集')
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='所属用户'),
    time = models.DateTimeField(verbose_name='时间',default=timezone.now)
    photo_url = models.FileField(verbose_name='图片地址',upload_to='photo/'),
    weather = models.CharField(verbose_name='天气标签',max_length=255),
    text_num = models.IntegerField(verbose_name='文字区文字个数'),
    color = models.CharField(verbose_name='图像主色调',max_length=255),
    mass_weight = models.FloatField(verbose_name='质量比重')
    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片表'
    def __str__(self):
        return "%s"% (self.photo_id)

class Template(models.Model):
    template_id = models.AutoField(verbose_name='模板号',primary_key=True),
    tag = models.CharField(verbose_name='模板标签',max_length=255,blank=True),
    models.FileField(verbose_name='模板背景',upload_to='template/'),
    text_num = models.IntegerField(verbose_name='文字区文字个数'),
    color = models.CharField(verbose_name='模板主色调',max_length=255),
    mass_weight = models.FloatField(verbose_name='图像大小参数')
    photo_num = models.IntegerField(verbose_name='容纳图片个数'),
    class Meta:
        verbose_name = '模板'
        verbose_name_plural = '模板表'
    def __str__(self):
        return "%s"% (self.template_id)
