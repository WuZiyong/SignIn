from django.conf.urls import url
from django.contrib import admin
from login import views
from django.urls import path
from django.conf.urls import handler404, handler500
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register_limited),
    #url(r'^register-admin/', views.register),
    url(r'^logout/', views.logout),
    url(r'^modify-password/', views.modify_password),
    path('404/', views.page_not_found, name='修改工作人员'),
    path('500/', views.page_error, name='修改工作人员'),
]