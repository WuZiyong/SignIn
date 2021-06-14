from django.db import models
from apps.file.util import *
import uuid
import django.utils.timezone as timezone
# Create your models here.

#学生类
class Student(models.Model):
    #学生姓名
    stu_name = models.CharField(
        '姓名', max_length=20, unique=False,default='unknown')
    #学生学号
    stu_id = models.CharField(
        '学号', max_length=10, unique=True, default='unknown')  # 学号唯一
    stu_grade = models.IntegerField(
        '年级', choices=grade_choices, null=False, default=1)
    create_time = models.DateTimeField(
        '创建时间', default=timezone.now, editable=False)

#活动数据库
class Meeting(models.Model):
    meet_uuid = models.UUIDField(
        'meet_uuid', default=uuid.uuid4, editable=False, unique=True)
    meet_theme = models.CharField(
        '活动主题', max_length=50, unique=False,default='')
    meet_name = models.CharField(
        '活动名称', max_length=50, unique=False)
    need_num = models.IntegerField('应到人数', default=0)
    exa_num = models.IntegerField('实到人数', default=0)
    need_grade = models.CharField(
        '应到年级', max_length=10, unique=False,default='123456789')
    meet_begin_time = models.DateTimeField(
        '活动开始时间',  null=True, blank=True)
    meet_end_time = models.DateTimeField(
        '活动结束时间',  null=True, blank=True)
    create_time = models.DateTimeField(
        '创建时间', default=timezone.now, editable=False)

#签到数据表
class Signlist(models.Model):
    stu_id = models.CharField(
        '学号', max_length=10, unique=False, default='unknown')  # 学号唯一
    stu_name = models.CharField(
        '姓名', max_length=20, unique=False, default='unknown')  
    meet_uuid = models.UUIDField(
        'meet_uuid', default=uuid.uuid4, editable=False, unique=False)


    
