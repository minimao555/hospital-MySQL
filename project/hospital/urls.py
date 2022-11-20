from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # login entry
    path("login/", views.login),
    # logout entry
    path("logout/", views.logout),
    # 请求一级目录，暂时与二级目录共用一个页面
    path('', views.index),
    # 请求二级目录，路径中间不能出现/（除非是第一或最后一个），如/test_model1/123
    re_path(r'^[/]?[^/]*?[/]?$', views.index),
    # 中间出现一个/，且最后是/change，则为请求具体的表单，如/test_model1/123/change
    re_path(r'^[/]?[^/]*?/[^/]*?/change[/]?$', views.form),
    # 最后是/add，则为添加，如/test_model1/add
    re_path(r'^[/]?[^/]*?/add[/]?$', views.addform),
    # 中间出现一个/，且最后是/delete，则为删除该表单，如/test_model1/123/delete
    re_path(r'^[/]?[^/]*?/[^/]*?/delete[/]?$', views.deleteform),
]
