from django.test import TestCase
from apps.login.models import User

# Create your tests here.


def init_basic_user():
    students = ['陈懿', '陈紫欣']
    teachers = ['范文娟', '吴嘉莉', '林婧', '钟儒发', '刘洋冬一', '刘艳芬',
                '董宇浩', '刘念', '王昕', '林伟鹏', '谷德峰', '张锦绣', '郝雅娟']

    pwd = '1'

    for i, users in enumerate([students, teachers]):
        level = [1, 2][i]
        department = ['plan', 'faculty'][i]
        for j, user in enumerate(users):
            user_d = {
                'name': user,
                'level': level,
                'department': department,
                'email': f"{i}{j}@test.sysu.edu.cn",
                'stu_id': f"{i}{j}",
                'password': pwd,
            }
            try:
                new_user = User.objects.create(**user_d)
                new_user.save()
            except Exception as e:
                print(user, e)

