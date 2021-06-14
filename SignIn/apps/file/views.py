from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils.http import urlquote
#from apps.logger import logger
import uuid
import json
from .models import FileInfo,grade_trans
from .forms import UploadForm
import os
from SignIn.settings import MEDIA_ROOT
import datetime
import pytz
import pandas as pd
from apps.sign.models import Student


def transfer_time(value, f):
    '''按格式化字符串转换时间格式'''
    dt = datetime.datetime.strptime(value, f)
    ts = int(dt.timestamp())
    t = datetime.datetime.fromtimestamp(
        ts, pytz.timezone('Asia/Shanghai'))
    # logger.info(value, dt, t)
    return dt

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        #upload_people = request.session.get('user_name')
        #logger.info('upload_people: ', upload_people)
        # 此次提交所有文件
        filelist=[]
        if form.is_valid():
            files = request.FILES.getlist('file')
            #获取文件年级归属
            grade = int(request.POST.get('grade'))
            print('grade: ',grade)
            #获取当前年级下的文件(后续可增加多个文件同时上传)
            current_file = FileInfo.objects.filter(grade = int(grade))
            upload_people=''
            #load 属性用以判断是否是csv excel格式
            load =False
            print('current_file: ', current_file)
            for f in files:
                rewrite=0
                if not current_file.exists():
                    # 添加 resource_uuid
                    uid = str(uuid.uuid4())
                    resource_uuid = ''.join(uid.split('-'))
                    print('resource_uuid: ',resource_uuid)
                else:
                    # 如果上传服务器已存在的相同年级的文件 则被认为修改服务器中相同年级的文件
                    modify_file = FileInfo.objects.get(file_name = f.name,grade = int(grade) )
                    print('modify_file: ',modify_file)
                    resource_uuid = modify_file.resource_uuid
                    print('modify_resources_uuid: ',resource_uuid)
                    modify_file.delete()
                    os.remove(modify_file.file_path)
                    print('-----modify_file deleted succsessfully-----')
                    rewrite=1
                try:
                    (file,filepath) = upload_file(grade, f,resource_uuid,upload_people)
                    data=None
                    # 判断是否有覆盖文件的问题
                    if rewrite==1:
                        data=delestu(grade=grade)
                    load=loadstufromfile(filepath=filepath,extension=file['file_name'].split('.')[-1],grade=grade)
                    filelist.append(file)
                    print('--new file saved---')
                except Exception as e:
                    # pass
                    print(e)
                    return HttpResponse(e)
            #返回上传页
            if data is None and load == True:
                data = {'files': filelist,'status':200}
            elif data is None and load == False:
                data = {'files': filelist,'status':400,'msg':'文件格式错误或年级不存在'}
            print('respond data: ',data)
            return JsonResponse(data)
        else:
            form = UploadForm()
            data = {'msg':'表单提交有误','status':402}
            return JsonResponse(data)
    else:
        data = {'msg': '请求方式错误', 'status': 400}
        return JsonResponse(data)



# 下载文件
def download(request,grade):
    if request.method == 'GET':
        #current_operator = request.session.get('user_name')
        #current_level = request.session.get('user_level')
        #logger.info('download resource_uuid: ', resource_uuid)
        #resource_uuid = ''.join(resource_uuid.split('-'))
        file_info = FileInfo.objects.filter(grade = grade)
        #判断文件是否存在
        if not file_info.exists():
            data = {'msg':'不存在此年级的名单','status':402}
            JsonResponse(data)
        #文件存在获取文件
        file_info = FileInfo.objects.get(grade = grade)
        print('下载文件名: ', file_info.file_name)
        print('file_info.file_path: ', file_info.file_path)

        #这里可以增加判断是否需要权限
        file = open(file_info.file_path,'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment;filename="%s"' %urlquote(file_info.file_name)
        response['msg'] = '成功'
        response['status'] = 200
        #return JsonResponse(response,safe=False)
        return response
    else:
        data = {'msg':'400'}
        return JsonResponse(data)

# 删除文件
def delete(request, resource_uuid):
    if request.method == 'GET':
        current_operator = request.session.get('user_name')
        current_level = request.session.get('user_level')
        logger.info('delete resource_uuid: ',resource_uuid)
        resource_uuid = ''.join(resource_uuid.split('-'))
        file_info = FileInfo.objects.get(resource_uuid=resource_uuid)
        if current_level > 0 or file_info.upload_people == current_operator:
            file_info.delete()
            data = {'msg': '200 ok', 'status': 200}
        else:
            data = {'msg':'权限不足','status':402}
    else:
        data = {'msg': '请求方式错误', 'status': 400}
    return JsonResponse(data)


# 资源数据库信息返回
def get_resource_info(resource_uuid=None, push_uuid=None, upload_people=None):
    if resource_uuid:
        ResourceData = FileInfo.objects.get(resource_uuid=resource_uuid)
    if push_uuid:
        ResourceData = FileInfo.objects.filter(push_uuid=push_uuid)
    if upload_people:
        ResourceData = FileInfo.objects.filter(upload_people=upload_people)
    return ResourceData

def upload_file(grade, f, suid, upload_people):
    if not os.path.exists(f"{MEDIA_ROOT}/resource/"):
        os.mkdir(f"{MEDIA_ROOT}/resource")
    if not os.path.exists(f"{MEDIA_ROOT}/resource/" + str(grade_trans[grade-1])):
        os.mkdir(f"{MEDIA_ROOT}/resource/" + str(grade_trans[grade-1]))
    file_path = os.path.join(f"{MEDIA_ROOT}/resource/" + str(grade_trans[grade-1]) + '/' +  f.name)
    print('file_path: ',file_path)
    upload_time = transfer_time(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
    print('upload_time: ',upload_time)
    file_info = FileInfo(file_name=f.name, file_size=1 if 0 < f.size < 1024 else f.size / 1024,upload_time=upload_time,
            file_path=file_path,resource_uuid=suid,grade=grade,upload_people = upload_people)
    file_info.save()
    file = {'file_name':f.name,'resource_uuid':suid,'operator_now':upload_people,'upload_time':upload_time,'grade':grade}
    #上传文件
    destination = open(file_path,'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    print('---file saved---')
    return (file,file_path)


#加载excel内数据创建学生 若不存在学生则创建 若存在则先删除再创建
def loadstufromfile(filepath,extension,grade):
    if extension == 'csv':
        df = pd.read_csv(filepath)
    elif extension == 'xls' or extension == 'xlsx':
        df = pd.read_excel(filepath)
    else:
        return False
    col = df.shape[1]
    df.columns = ['name','id']+list(range(col-2))
    names = df['name']
    ids = df['id']
    lens = df.shape[0]
    if not addtoalnumtofile(lens,grade):
        return False
    for index in range(lens):
        student = Student.objects.filter(stu_id=ids[index])
        if student.exists():
            #student = Student.objects.get(stu_id=ids[index])
            student.delete()
        student = Student(stu_name=names[index],stu_id=ids[index],stu_grade=grade)
        student.save()
    return True



#添加年级总人数
def addtoalnumtofile(totalnum,grade):
    try:
        file_info=FileInfo.objects.get(grade=grade)
        file_info.total_num = totalnum
        file_info.save()
        return True
    except:
        return False
    

#按照年级/学号删除学生 返回data
def delestu(grade=None,id=None):
    data = {
        'msg':'成功',
        'status':200,
    }
    if not grade is None:
        student=Student.objects.filter(stu_grade=grade)
        if student.exists():
            student.delete()
        else:
            data = {
                'msg':'年级输入有误',
                'status':404,
            }
    if not id is None:
        student=Student.objects.filter(stu_id=id)
        if student.exists():
            student.delete()
        else:
            data = {
                'msg':'学号输入有误',
                'status':404,
            }
    if grade is None and id is None:
        data = {
                'msg':'无输入信息',
                'status':404,
            }

    return data





        

        





