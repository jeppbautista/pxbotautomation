from django.urls import path
from django.views import generic
from . import views
from .views import DashView, UserView, UserEditView, UserCreateView


app_name = 'dashboard'
urlpatterns =[
    path('', DashView.as_view(), name='index'),
    path('users/', UserView.as_view(), name='users'),
    path('users/<int:pk>/', UserEditView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('automation/', views.selenium_automation, name='automation'),
    path('expiration/', views.expiration, name='expiration')
]