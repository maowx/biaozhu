from django.db import models
from django.db.models import Q
from django.http import request
from django.http import HttpRequest
from django.utils import timezone
from django.utils.safestring import mark_safe
from datetime import datetime

# Create your models here.


class User(models.Model):
    TYPE_CHOICES = (
        (0, '标注用户'),
        (1, '测试用户'),
        (2, '管理员用户'),
        (3, '超级管理员')
    )
    STATUS = (
        (0, '正常'),
        (1, '已拉黑')
    )
    username = models.CharField('用户名', max_length=50)
    password = models.CharField('密码', max_length=50)
    email = models.EmailField('邮箱')
    operator = models.IntegerField('角色', default=0, choices=TYPE_CHOICES)  # 0表示用户，1表示管理员
    last_login_ip = models.CharField('最后登录IP', null=True, blank=True, editable=False, max_length=50)
    last_login_time = models.DateTimeField('最后登录时间', null=True, blank=True, editable=False)
    status = models.IntegerField('状态', default=0, editable=False, choices=STATUS)  # 0表示正常，1表示已拉黑

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u"用户组"

    def __str__(self):
        return self.username


class Group(models.Model):
    group_name = models.CharField('标签名称', max_length=200)

    class Meta:
        verbose_name = u'标签管理'
        verbose_name_plural = u"标签管理"

    def __str__(self):
        return self.group_name


class Pool(models.Model):
    title = models.CharField('标题', max_length=200)
    picture = models.ImageField('图片', upload_to='img')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, choices=Group.objects.all().values_list('id', 'group_name'), verbose_name='标签')

    def image_tag(self):
        return mark_safe('<a href="%s"><img src="/static/image/img_icon.jpg"  width="20px"/>' % self.picture.url)
    image_tag.short_description = '图片'
    image_tag.allow_tags = True

    def my_property(self):
        return Group.objects.filter(id=self.group_id).values()[0]['group_name']
    my_property.short_description = '标签'
    group_name = property(my_property)

    class Meta:
        verbose_name = u'图片管理'
        verbose_name_plural = u"图片管理"

    def __str__(self):
        return self.title


class Choice(models.Model):
    TYPE_CHOICES = (
        (1, '左图更优'),
        (2, '右图更优'),
        (3, '两图相似')
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE, choices=User.objects.all().values_list('id', 'username'), verbose_name='标注人员', editable=False)
    use_time = models.IntegerField('使用时间', editable=False)
    left_pic_id = models.IntegerField(editable=False)
    right_pic_id = models.IntegerField(editable=False)
    choice_num = models.IntegerField('选择图片', choices=TYPE_CHOICES, editable=False)  # 1表示左图更优 2表示右图更优 3表示两图相近
    choose_time = models.DateTimeField('操作时间', auto_now_add=True, editable=False)

    def user_name(self):
        return User.objects.filter(id=self.user_id).values()[0]['username']
    user_name.short_description = '标注人员'
    username = property(user_name)

    def left_title(self):
        return Pool.objects.filter(id=self.left_pic_id).values()[0]['title']
    left_title.short_description = '左图名称'
    leftTitle = property(left_title)

    def left_pic(self):
        return mark_safe('<a href="%s"><img src="/static/image/img_icon.jpg"  width="20px"/>' %
                         Pool.objects.get(id=self.left_pic_id).picture.url)
    left_pic.short_description = '左图'
    left_pic.allow_tags = True

    def right_title(self):
        return Pool.objects.filter(id=self.right_pic_id).values()[0]['title']
    right_title.short_description = '右图名称'
    rightTitle = property(right_title)

    def right_pic(self):

        return mark_safe('<a href="%s"><img src="/static/image/img_icon.jpg"  width="20px"/>' %
                         Pool.objects.get(id=self.right_pic_id).picture.url)
    right_pic.short_description = '右图'
    right_pic.allow_tags = True

    class Meta:
        verbose_name = u'标注信息'
        verbose_name_plural = u"标注信息"


class Dictionary(models.Model):
    data_name = models.CharField('data_name', max_length=255)
    data_value = models.CharField('data_value', max_length=255)
    create_time = models.DateTimeField('create_time', auto_now_add=True)



