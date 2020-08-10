"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from maps import views

schema_admin_view = get_schema_view(
    openapi.Info(
        title="여행 API(Admin)",
        default_version='version1',
        description="여행 정보 관리 및 유저 관리, 댓글 관리|(추가 예정)",
        terms_of_service="https://lab.ssafy.com/dongqda/traveltokorea.git",
        contact=openapi.Contact(email="no"),
        license=openapi.License(name="SSAFY"),
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser)
)

schema_view = get_schema_view(
    openapi.Info(
        title="여행 API",
        default_version='version 1',
        description="여행 정보 가져 오기",
        terms_of_service="https://lab.ssafy.com/dongqda/traveltokorea.git",
        # 이메일 형식 안맞으면 internal error 발생함
        contact=openapi.Contact(email="no"),
        license=openapi.License(name="SSAFY"),
    ),
    # validators=['flex', 'ssv'],

    # public = True면 모든 API가 권한에 상관없이 보여짐
    # False 로 설정해서 권한이 없는 API는 볼 수 없게함
    # 영화 & 배우 데이터를 저장하는건 관리자만 가능함
    # public=False,
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    # Public API
    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Admin API 
    path('admin/api/doc/', login_required(schema_admin_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('admin/api/doc/redoc/', login_required(schema_admin_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    # path('accounts/', login_required(include('accounts.urls'))),

    # app
    path('admin/', admin.site.urls),
    path('maps/', include('maps.urls')),
    path('myaccounts/', include('myaccounts.urls')),
    path('', views.main),
    # path('social/', include('social.apps.django_app.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
]   
