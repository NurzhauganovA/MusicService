from django.urls import path
from . import views

urlpatterns = [
    path('', views.firstpage, name='first'),
    path('home', views.index, name='home'),

]
