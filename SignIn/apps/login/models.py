from django.db import models
# from django_mysql.models import models


class User(models.Model):
    '''用户表'''

    name = models.CharField('姓名', max_length=128, unique=False)  # 名字可以重复
    email = models.EmailField('邮箱', unique=True, default='unknown')
    teach_id = models.CharField(
        '学号', max_length=10, unique=True, default='unknown')  # 学号唯一
    password = models.CharField('密码', max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}({})".format(self.name, self.teach_id)

    class Meta:
        db_table = 'user'
        ordering = ['create_time']