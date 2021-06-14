from apps.file.views import transfer_time
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import uuid
import json
from .models import Meeting,Signlist, Student
from math import ceil
from apps.file.util import SERVER_IP
from datetime import datetime
from pytz import timezone 
from apps.file.models import FileInfo
from apps.file.util import grade_trans,PUSH_PER_PAGE,MAX_PAGES_SHOW_NUM
# Create your views here.
import pandas as pd
from SignIn.settings import MEDIA_ROOT
import os 
from django.http import FileResponse
from django.utils.http import urlquote



def ormToJson(ormData):
    '''数据转换器'''
    jsonData = serializers.serialize("json", ormData)
    data = json.loads(jsonData)
    return data



def main(request):
    '''应用主页面渲染'''
    #print(status)
    page_num = request.GET.get('pgn')
    meet_info = Meeting.objects.filter().order_by('create_time')
    transfer_data = prepare_data_with_pages(meet_info, page_num)
    #print('Hello World!')
    # test_push_insert_new_line()
    return render(request, "main.pug",transfer_data)
    #return render(request, "index.html")

def createmeet(request):
    '''生成活动页面渲染'''
    #print(status)
    #print('Hello World!')
    # test_push_insert_new_line()
    return render(request, "createmeet.pug")

def signin(request,meet_uuid):
    '''签到页面渲染'''
    (data,state)=getMeetingDetail(meet_uuid)
    if state:
        if SERVER_IP == '':
            serverip = ''
        else:
            serverip = f"http://{SERVER_IP}"
        data['fields']['url']=serverip+'/signin/'+data['fields']['meet_uuid']
        print('meet["url"]: ',data['fields']['url'])
        data['signin']=1
        return render(request, "signin.pug",data)
    else:
        return JsonResponse(data)
    #return render(request, "index.html")

def changetimeformat(time):
    '''改变时间输出格式'''
    return time.split('T')[0]+' '+time.split('T')[1].split('Z')[0]

def getMeetingDetail(meet_uuid):
    state = False
    try:
        meet_info = Meeting.objects.filter(meet_uuid=meet_uuid)
        data = ormToJson(meet_info)[0]
        begin_t0 = data['fields']['meet_begin_time']
        end_t0 = data['fields']['meet_end_time']
        data['fields']['meet_begin_time'] = changetimeformat(begin_t0)
        data['fields']['meet_end_time'] = changetimeformat(end_t0)
        state = True
    except Exception as e:
        print(e)
        data = {
            'msg':'不存在此活动信息',
            'status':404,
        }
    return (data,state)
    


def meetdetail(request,meet_uuid):
    '''详情页面渲染'''
    (data,state)=getMeetingDetail(meet_uuid)
    if state:
        if SERVER_IP == '':
            serverip = ''
        else:
            serverip = f"http://{SERVER_IP}"
        data['fields']['url']=serverip+'/signin/'+data['fields']['meet_uuid']
        print('meet["url"]: ',data['fields']['url'])
        print(data)
    else:
        return JsonResponse(data)
    return render(request,"meetdetail.pug",data)


def prepare_data_with_pages(pushData, page_num, push_per_page=PUSH_PER_PAGE, max_pages_show_num=MAX_PAGES_SHOW_NUM):
    '''准备渲染所需数据
    1. 多页显示
    '''
    if len(pushData) == 0:
        return {
            'num': 0,
        }
    try:
        page_num = int(page_num)
    except:
        page_num = 0
    # page_num = 0 if not isinstance(page_num, int) else
    # logger.info(page_num)
    length = ceil(len(pushData) / push_per_page)  # 总页数
    page_num = min(length - 1, page_num)  # 防止超页码

    # 数据切分
    if page_num < length - 1:
        output_data = pushData[page_num *
                               push_per_page:(page_num + 1) * push_per_page]
    else:
        output_data = pushData[page_num * push_per_page:]

    # 翻页显示处理
    pages_begin = max(0, page_num - max_pages_show_num)
    pages_end = min(length-1, page_num + max_pages_show_num)
    page_nums = list(range(pages_begin+1,
                           pages_end + 2))

    # 页面渲染数据
    index = 0
    ids = list(range(page_num * push_per_page+1,(page_num + 1) * push_per_page+1))
    data = ormToJson(output_data)
    for meet in data:
        meet = meet['fields']
        meet['id'] = ids[index]
        meet['meet_begin_time']=changetimeformat(meet['meet_begin_time'])
        meet['meet_end_time']=changetimeformat(meet['meet_end_time'])
        
        print('meet["meet_begin_time"]: ',meet['meet_begin_time'])
        index+=1
    print('=======================================')
    print('begin: ',pages_begin)
    print('end: ',pages_end)
    print('page_num_list: ',page_nums)
    print('begin_judge: ',max_pages_show_num)
    print('end_judge: ',length - max_pages_show_num-1)


    transfer_data = {
        'num': len(output_data),
        'data': data,
        'page_num': page_num,
        'page_num_list': page_nums,
        'begin': pages_begin,
        'end': pages_end,
        'begin_judge': max_pages_show_num,
        'end_judge': length - max_pages_show_num-1,
        'len': length,
    }
    return transfer_data

def newmeet(request):
    '''新的活动提交'''
    if request.method == 'POST':
        post = request.POST
        #添加meet_uuid
        uid = str(uuid.uuid4())
        meet_uuid = ''.join(uid.split('-'))
        print('meet_uuid: ',meet_uuid)
        #获取应到人数
        need_grades=list(post.get('new_need_grade'))
        total_num = 0
        #判断是否存在有某些年级不存在文件的情况
        none = False
        #将不存在的年级放入list中
        none_list = []
        none_list_zh=[]
        #将所有需要的年级的人加起来
        for need_grade in need_grades:
            tot = getToalNum(int(need_grade))
            if not tot is None:
                total_num += tot
            else:
                total_num +=0
                none = True
                none_list.append(int(need_grade))
        if none:
            for grade in none_list:
                none_list_zh.append(grade_trans[grade-1])
        #统计人数后创建新的活动到数据库中
        create=createNewMeet(meet_uuid,post.get('meet_theme'),post.get('meet_name'),post.get('meet_begin_time'),post.get('meet_end_time'),need_grade=post.get('new_need_grade'),need_num=total_num)
        if create:
            data = {
                'msg': '存在无学生年级:'+'、'.join(none_list_zh) if none else '提交成功',
                'status': 200,
                'meet_uuid': meet_uuid,
                'meet_theme':post.get('meet_theme'),
                'meet_name':post.get('meet_name'),
                'need_grade':post.get('new_need_grade'),
                'total_num':total_num,
            }
        else:
            data = {
                'msg':'创建活动失败',
                'status': 400,
            }
        return JsonResponse(data)
    else:
        data = {'msg': '请求方式错误', 'status': 400}
        return JsonResponse(data)


def newsign(request):
    '''新的活动提交'''
    if request.method == 'POST':
        post = request.POST
        stu_id = post.get('stu_id')
        stu_name = post.get('stu_name')
        meet_uuid = post.get('meet_uuid')
        #判断活动是否存在 若存在判断签到时间是否在活动时间内
        try:
            meet_info=Meeting.objects.get(meet_uuid=meet_uuid)
        except:
            data = {
                'msg':'活动不存在',
                'status': 404,
            }
            return JsonResponse(data)
        meet_begin_time = meet_info.meet_begin_time#.strftime('%Y-%m-%d %H:%M:%S')
        meet_end_time = meet_info.meet_end_time#.strftime('%Y-%m-%d %H:%M:%S')
        cst_tz = timezone('Asia/Shanghai')
        now = datetime.now().astimezone(cst_tz)#.strftime('%Y-%m-%d %H:%M:%S')  
        print('===============================================')
        print('meet_begin_time: ',meet_begin_time)
        print('meet_end_time: ',meet_end_time)
        print('now: ',now)
        if meet_begin_time > now or now > meet_end_time:
            data = {
                'msg': '活动未开始或活动已结束',
                'status': 302,
            }
            return JsonResponse(data)
        # 判断此学生是否在数据库中
        stu_info = Student.objects.filter(stu_id=stu_id,stu_name=stu_name)
        if stu_info.exists():
            #先判断此学生在当前活动下是否已经签到过了
            signin_info=Signlist.objects.filter(meet_uuid=meet_uuid,stu_id=stu_id)
            if not signin_info.exists():
                create=createNewSignlist(meet_uuid,stu_id,stu_name)
                if create:
                    meet_info.exa_num +=1
                    meet_info.save()
                    data = {
                        'msg': '签到成功',
                        'status': 200,
                    }
                else:
                    data = {
                        'msg':'签到失败',
                        'status': 400,
                    }
            else:
                data = {
                'msg':'请勿重复签到',
                'status': 300,
                }   
        else:
            data = {
                'msg':'姓名学号填写错误或姓名学号不存在',
                'status': 404,
                }
            
        
        return JsonResponse(data)
    else:
        data = {'msg': '请求方式错误', 'status': 400}
        return JsonResponse(data)




#获取年级总人数
def getToalNum(grade):
    try:
        file_info=FileInfo.objects.get(grade=grade)
        return file_info.total_num
    except:
        print('年级文件不存在')
        return None


def createNewMeet(meet_uuid,meet_theme,meet_name,meet_begin_time,meet_end_time,need_grade='123456789',need_num=0):
    '''创建新的活动'''
    newmeet={
        'meet_uuid':meet_uuid,
        'meet_theme':meet_theme,
        'meet_name':meet_name,
        'meet_begin_time': meet_begin_time,
        'meet_end_time':meet_end_time,
        'need_grade':need_grade,
        'need_num':need_num,
        'exa_num':0,
    }
    try:
        _newmeetinfo=Meeting.objects.create(**newmeet)
        _newmeetinfo.save()
        flag=True
    except Exception as e:
        print(e)
        flag=False
    return flag


def createNewSignlist(meet_uuid,stu_id,stu_name):
    '''创建新的签到'''
    newsignlist={
        'meet_uuid':meet_uuid,
        'stu_id':stu_id,
        'stu_name':stu_name,
    }
    try:
        _newsignlistinfo=Signlist.objects.create(**newsignlist)
        _newsignlistinfo.save()
        flag=True
    except Exception as e:
        print(e)
        flag=False
    return flag


def meetdownload(request):
    '''下载签到缺勤名单'''
    if request.method == 'GET':
        Get = request.GET
        meet_uuid = Get.get('meet_uuid')
        download_type = int(Get.get('type'))
        print('meet_uuid: ',meet_uuid)
        print('download_type: ',download_type)
        #判断是否存在这一活动
        try:
            meet_info = Meeting.objects.get(meet_uuid=meet_uuid)
        except Exception as e:
            print(e)
            data = {'msg': '活动不存在', 'status':404}
            return JsonResponse(data)

        # 签到名单下载
        if download_type == 1:
            df,filename = createSignTable(meet_info,meet_uuid)
            response = fileresponse(df,filename,meet_info,'签到')
            return response
        #缺勤名单下载
        else:
            #获取当前活动下所有需要签到的学生名单
            df,filename = createUnSignTable(meet_info,meet_uuid)
            response = fileresponse(df,filename,meet_info,'缺勤')
            return response
    else:
        data = {'msg':'400'}
        return JsonResponse(data)

def fileresponse(df,filename,meet_info,name):
    df.to_csv(filename)
    #这里可以增加判断是否需要权限
    file = open(filename,'rb')
    response = FileResponse(file)
    response['Content-Disposition'] = 'attachment;filename="%s"' %urlquote(meet_info.meet_name+name+'名单.csv')
    response['msg'] = '成功'
    response['status'] = 200
    #return JsonResponse(response,safe=False)
    return response

def createSignTable(meet_info,meet_uuid):
    '''创建签到名单'''
    filepath = makdirmeet(meet_uuid)
    signin_info = Signlist.objects.filter(meet_uuid=meet_uuid)
    signin_stus = {
        'stu_name':[],
        'stu_id':[],
    }
    for sign_stu in signin_info:
        signin_stus['stu_name'].append(sign_stu.stu_name)
        signin_stus['stu_id'].append(sign_stu.stu_id)
    print('signin_stus: ',signin_stus)
    df = pd.DataFrame(signin_stus)
    df.columns = ['姓名','学号']
    filename = filepath+meet_info.meet_name+'签到名单.csv'
    return df,filename

def createUnSignTable(meet_info,meet_uuid):
    '''创建缺勤名单'''
    filepath = makdirmeet(meet_uuid)
    stu_info = Student.objects.filter(stu_grade__in=[int(xx) for xx in list(meet_info.need_grade)])
    df,filename = createSignTable(meet_info,meet_uuid)
    unsignin_stus = {
        'stu_name':[],
        'stu_id':[],
    }
    df_id_list= list(df['学号'])
    for stu in stu_info:
        if not stu.stu_id in df_id_list:
            unsignin_stus['stu_name'].append(stu.stu_name)
            unsignin_stus['stu_id'].append(stu.stu_id)
    print('unsignin_stus: ',unsignin_stus)
    df = pd.DataFrame(unsignin_stus)
    df.columns = ['姓名','学号']
    filename = filepath+meet_info.meet_name+'缺勤名单.csv'
    return df,filename

def makdirmeet(meet_uuid):
    '''判断meeting的路径是否存在'''
    if not os.path.exists(f"{MEDIA_ROOT}/resource/"):
        os.mkdir(f"{MEDIA_ROOT}/resource")
    if not os.path.exists(f"{MEDIA_ROOT}/resource/meeting"):
        os.mkdir(f"{MEDIA_ROOT}/resource/meeting")
    if not os.path.exists(f"{MEDIA_ROOT}/resource/meeting/{meet_uuid}"):
        os.mkdir(f"{MEDIA_ROOT}/resource/meeting/{meet_uuid}")
    return f"{MEDIA_ROOT}/resource/meeting/{meet_uuid}/"
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


