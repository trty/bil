from django.urls import path
from . import views

urlpatterns = [
    # 直接加载
    path("add/", views.Add.as_view()),
    path("info/", views.Info.as_view()),
    # 异步加载
    path("add_sync/", views.AddSync.as_view()),
    path("info_sync/", views.InfoSync.as_view()),
]