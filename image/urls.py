# coding=utf-8
from django.conf.urls import url
from image import views

app_name = 'image'

urlpatterns = [
    url(r'^images-list/$', views.list_images, name='images_list'),
    url(r'^upload-image/$', views.upload_image, name='upload_image'),
    url(r'^del-image/$', views.del_image, name='del_image'),
    url(r'^images/$', views.images_fall, name='images_fall'),
]
