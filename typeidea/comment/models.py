# -*- coding: UTF-8 -*-

from django.db import models
from blog.models import Post

# Create your models here.


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    target = models.CharField(max_length=100, verbose_name='评论目标')
    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=500, verbose_name='昵称')
    # URLField：继承自CharField，实现对URL的特殊处理
    website = models.URLField(verbose_name='网站')
    # EmailField：继承自CharField，实现对Email的特殊处理
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return self.target

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)