from django.urls import path, include
from . import views


urlpatterns = [
  #  path('', views.index, name='index'),
    path('', views.landing, name='landing'),
    path('register', views.register, name='register'),
    path('testing', views.testing, name='testing'),
    path('loginview', views.login_view, name='login_view'),
    path('registerview', views.register_view, name='register_view'),
    path('logoutview', views.logout_view, name='logout_view'),
    path('AvailableCoursesview', views.AvailableCourses_view, name='AvailableCourses_view'), 
    path('displayCourseview/<str:csrid>', views.displayCourse_view, name='displayCourse_view'), 
    path('download', views.export_users_xls, name='export_users_xls'),
      
]
