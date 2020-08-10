from django.urls import path
from . import views

app_name = 'myaccounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # path('signinpage/', views.signinpage, name='signinpage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),

    # API Link(Only Admin)
    path('user/', views.UserGetSerializer),
    path('user/<str:email>/', views.UserInfoserializer, name='UserInfo'),
    ]

