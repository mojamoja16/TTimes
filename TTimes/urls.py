from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signupview, name='signup'),
    path('login/', loginview, name='login'),
    path('attendance/', attendanceview, name='attendance'),
    path('sample/', sampleview, name='sample'),
]
