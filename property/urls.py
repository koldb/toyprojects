from django.urls import path
from . import views

app_name ='property'

urlpatterns = [
    path('', views.index, name='index'),
    path('naver_excel', views.naver_excel, name='naver_excel'),
    path('naver_news_insert', views.naver_news_insert, name='naver_news_insert'),
    path('naver_list', views.naver_list, name='naver_list'),
    path('naver_view/<int:pk>/', views.naver_view, name='naver_view'),
    path('comment_create/<int:pk>/', views.comment_create, name='comment_create'),
    path('comment_modify/', views.comment_modify, name='comment_modify'),
    path('com_delete/<int:no>/<int:qno>/', views.com_delete, name='com_delete'),

]