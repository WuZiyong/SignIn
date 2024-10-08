# Generated by Django 3.0.2 on 2021-06-12 14:35

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='meet_uuid')),
                ('meet_name', models.CharField(max_length=50, verbose_name='姓名')),
                ('max_num', models.IntegerField(default=0, verbose_name='应到人数')),
                ('meet_begin_time', models.DateTimeField(blank=True, null=True, verbose_name='活动开始时间')),
                ('meet_end_time', models.DateTimeField(blank=True, null=True, verbose_name='活动结束时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='signlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(default='unknown', max_length=10, unique=True, verbose_name='学号')),
                ('meet_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='meet_uuid')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_name', models.CharField(max_length=20, verbose_name='姓名')),
                ('stu_id', models.CharField(default='unknown', max_length=10, unique=True, verbose_name='学号')),
                ('stu_grade', models.IntegerField(choices=[(1, '大一'), (2, '大二'), (3, '大三'), (4, '大四'), (5, '研一'), (6, '研二'), (7, '研三'), (8, '研四'), (9, '研五')], default=1, verbose_name='年级')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='创建时间')),
            ],
        ),
    ]
