from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name="Home"),
    path('login',views.login_user,name="LogIn"),
    path('timeline',views.timeline,name="TimeLine"),
    path('notes', views.notes, name="notes"),
    path("informer/", views.informer, name="informer"),
    path("attendance", views.attendance, name="attendance"),
    path('test',views.test,name="test"),   
]
