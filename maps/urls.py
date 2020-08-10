from django.urls import path
from . import views
from django.conf.urls import url, include

app_name = 'maps'
urlpatterns = [

    path('', views.main, name='main'),
    path('map/update/', views.detailcommon, name="detailcommon"),
    path('travelreview/', views.travelreview, name='travelreview'),
    path('travelreview/delete/<int:score_id>', views.deletereview, name='deletereview'),
    path('detail/<int:detail_id>/', views.detailpage, name="detailpage"),
    path('bookmark/<int:detail_id>', views.bookmark, name="bookmark"),
    path('score/<int:detail_id>/', views.scoreboard, name="scoreboard"),
    path('addscore/<int:detail_id>/', views.addscore, name="addscore"),
    path('comment/<int:detail_id>/', views.create_comment, name="create_comment"),

    #API update
    path('commonupdate/', views.detailcommon, name="detailcommon"),
    path('detailupdate/', views.detaildetail, name="detaildetail"),
    path('detailcontentupdate/', views.detailcontent, name="detailcontent"),


    # API Link
    path('common/', views.commonserializers),
    path('detail/', views.detailserializers),
    path('score/', views.scoreserailizers),
    path('category/<int:category>/', views.searchbycategoryserializers),
    path('area/<int:area>/category/<int:category>/', views.searchbyareaserializers),
    path('area/<int:area>/sigungu/<int:sigungu>/category/<int:category>/', views.searchbysigunguserializers),
    path('contentid/<int:contentid>/', views.searchbycontentidserializers),
]

