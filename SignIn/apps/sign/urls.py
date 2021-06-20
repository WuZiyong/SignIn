from django.urls import path
from . import views
#import NMIW_SPA.database as database

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('createmeet/', views.createmeet, name='createmeet'),
    path('meetdetail/<meet_uuid>', views.meetdetail, name='meetdetail'),
    path('signin/<meet_uuid>', views.signin, name='signin'),
    path('sign/newmeet/', views.newmeet, name='newmeet'),
    path('sign/newsign/', views.newsign, name='newmeet'),
    path('meet/download/', views.meetdownload, name='newmeet'),
    path('meet/delete/<meet_uuid>', views.deletemeet, name='newmeet'),
    
    
]