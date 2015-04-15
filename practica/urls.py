from django.conf.urls import patterns, url
from practica import views

urlpatterns = patterns('',
                       url(r'^$', views.inicio, name='inicio'),
                       url(r'registro/', views.registro, name='registro'),
                       url(r'login/', views.login, name='login'),
                       url(r'bienvenida/', views.bienvenida, name='bienvenida'),
                       url(r'etsiit/', views.etsiit, name='etsiit'),
                       url(r'imagenes/', views.imagenes, name='imagenes'),
                       url(r'buscador/', views.buscador, name='buscador'),
                       )