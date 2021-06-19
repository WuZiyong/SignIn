from django.shortcuts import render, redirect
from apps.login.models import User
from .forms import UserForm, RegisterForm
from django.http import HttpResponse, JsonResponse
import hashlib
#from apps.login.tests import init_basic_user


def hash_code(s, salt='nmiw'):
    '''密码加密'''
    return s
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    # init_basic_user()
    # if request.session['is_login']:
    #     return redirect("/")
    data = {
        'signin':2, 
    }
    return render(request, 'index.pug',data)


def register_limited(request):
    return register(request)


def register(request):

    signin = 2
    # try:
    #     if request.session['user_level'] < 2:
    #         return redirect('/index/')
    # except:
    #     pass
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！🧐"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            teach_id = register_form.cleaned_data['teach_id']
            email = register_form.cleaned_data['email']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不一致！❌"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if User.objects.filter(teach_id=teach_id):  # 用户名唯一
                    message = '这个账号已被注册🌝'
                    return render(request, 'login/register.pug', locals())
                if email.split('@')[-1][-12:] != '.sysu.edu.cn':
                    message = '请输入正确的中大邮箱🌚'
                    return render(request, 'login/register.pug', locals())
                if User.objects.filter(email=email):
                    message = '这个中大邮箱已被注册🌝'
                    return render(request, 'login/register.pug', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！😅'
                    return render(request, 'login/register.pug', locals())

                # 当一切都OK的情况下，创建新用户
                # print("\n\n\nteach_id ", teach_id)

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.teach_id = teach_id
                new_user.email = email
                new_user.save()
                return login(request, '注册成功，请登录😎')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.pug', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    request.session.flush()  # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/")


def modify_password(request):
    if not request.session.get('is_login', None):
        return redirect('/index')
    if request.method == "POST":
        print('===================')
        post = request.POST
        original_pwd = post.get('original_pwd')
        new_pwd1 = post.get('new_pwd1')
        new_pwd2 = post.get('new_pwd2')
        print(original_pwd)
        print(new_pwd1)
        print(new_pwd2)
        if new_pwd1 != new_pwd2:
            message = "两次输入的密码不一致！😅"
            return render(request, 'modify_password.pug', locals())
        if original_pwd == new_pwd1:
            message = "新旧密码咋能一样呢？！😯"
            return render(request, 'modify_password.pug', locals())
        user = User.objects.get(name=request.session['user_name'])
        if user.password == hash_code(original_pwd):
            user.password = hash_code(new_pwd1)
            #print('=========================')
            #print(hash_code(new_pwd1))
            user.save()
            request.session.flush()  # logout
            message = "密码修改成功！请重新登录😁"
            return login(request, message)

        else:
            message = "密码不正确哦🧐"
    return render(request, 'modify_password.pug', locals())


def login(request, message=""):
    # 不允许重复登录
    signin = 2

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = message if message else "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):
                    # 用户状态与数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.teach_id
                    request.session['user_name'] = user.name
                    message = "welcome!"
                    return redirect('/main/')
                else:
                    message = "密码不正确！"
            except Exception as e:
                print("except"+str(e))
                message = "用户不存在！"
        return render(request, 'login.pug', locals())

    login_form = UserForm()
    return render(request, 'login.pug', locals())


def get_user_info(user_names=None, user_email=None, user_teach_id=None):
    unknown_name = []
    pass_name = []
    if user_names:
        UserDatas = []
        if type(user_names) != list:
            user_names = [user_names]
        for user_name in user_names:
            try:
                UserData = User.objects.get(name=user_name)
                UserDatas.append(UserData)
                pass_name.append(user_name)
            except:
                unknown_name.append(user_name)
    elif user_email:
        UserDatas = User.objects.get(email=user_email)
    elif user_teach_id:
        UserDatas = User.objects.get(teach_id=user_teach_id)
    else:
        return None
    print('unknonw_name: ', unknown_name)
    unknown_name = '、'.join(unknown_name)
    print('pass_name: ', pass_name)
    pass_name = '、'.join(pass_name)
    return UserDatas, unknown_name, pass_name


def page_not_found(request, exception=None, template_name='404.pug'):
    return render(request, template_name)


def page_error(request, template_name='500.pug'):
    return render(request, template_name)