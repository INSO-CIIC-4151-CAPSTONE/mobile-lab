from django.urls import path
from . import views

urlpatterns = {
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('catalog/', views.test_view, name='catalog'),
    path('request/', views.createTestRequest, name='request'),
    path('update_request/<str:id>', views.updateTestRequest, name='update_request'),
    path('delete_request/<str:id>', views.deleteTestRequest, name='delete_request')
}
