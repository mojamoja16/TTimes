from django.contrib import admin
from django.urls import path
from .views import *

app_name = "TTimes"

urlpatterns = [
    path('login/', loginview, name='login'),
    path('attendance/', attendanceview, name='attendance'),
    path('staffpayment/', staffpaymentview, name='staffpayment'),
    path('dailylist/', dailylistview, name='dailylist'),
    path('staff/record/<int:employee_number>/', staffrecordview, name='staffrecord'),       
    path('attendance/manage/<int:pk>/',manageattendanceview, name='manage_attendance'),
    path('register/', RegisterStaffView.as_view(), name='register'),
    path('upload/', uploadview, name='upload'),
    path('download/', downloadview, name='download'),
]
