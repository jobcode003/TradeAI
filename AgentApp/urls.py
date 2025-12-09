from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('api/chat/', views.api_chat, name='api_chat'),
]
