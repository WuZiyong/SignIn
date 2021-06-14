from django.urls import path

from . import views

app_name = 'file'
  
urlpatterns = [
 path('resource/upload', views.upload, name='upload'), # 上传
 path('resource/download/<grade>', views.download, name='download'), # 下载
 #path('resource/delete/<grade>', views.delete, name='delete'), # 删除
]