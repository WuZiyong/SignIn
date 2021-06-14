from django.db import models
from django.utils import timezone
import uuid
# Create your models here.
from .util import *




class FileInfo(models.Model):



    '''文件记录'''
    resource_uuid = models.UUIDField(
        'resource_uuid', default=uuid.uuid4, editable=False, unique=True)
    #代表的年级
    grade = models.IntegerField(
        '年级', choices=grade_choices, null=False, default=1)
    # upload_people 上传者
    upload_people = models.CharField(max_length=500, default='')
    #年级总人数
    total_num = models.IntegerField(
        '年级总人数', null=False, default=0)
    file_name = models.CharField(max_length=500)
    file_size = models.DecimalField(max_digits=10, decimal_places=0)
    file_path = models.CharField(max_length=500)
    upload_time = models.DateTimeField('提交时间', auto_now_add=True)