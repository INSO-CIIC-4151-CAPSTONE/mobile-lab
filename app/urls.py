from django.urls import path
from . import views

''' © 2022 Mobile-Lab, All Rights Reserved. '''

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('usercontact/', views.user_contact_page, name='usercontact'),
    path('catalog/', views.labTests, name='catalog'),
    path('request/<str:id>', views.createTestRequest, name='request'),
    path('testsList/', views.testList_page, name='testList')

]
