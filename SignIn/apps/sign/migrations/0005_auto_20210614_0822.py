# Generated by Django 3.0.2 on 2021-06-14 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0004_auto_20210614_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='signlist',
            name='stu_name',
            field=models.CharField(default='unknown', max_length=20, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='student',
            name='stu_name',
            field=models.CharField(default='unknown', max_length=20, verbose_name='姓名'),
        ),
    ]
