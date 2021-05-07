from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
# from .models import SubmitAttendance
# from .forms import SubmitAttendanceForm
from datetime import datetime
from django.utils import timezone
from django.views.generic import TemplateView
from .models import *
from .forms import StaffAttendanceForm


# Define my function here.
import datetime
import pytz

def delta2chunk(delta: datetime.timedelta, chunk = 30):
    h, m, _ = str(delta).split(":")
    minutes = int(h) * 60 + int(m)
    return minutes // chunk

# Create your views here.
def signupview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            User.objects.create_user(username_data, '', password_data)
        except IntegrityError:
            return render(request, 'signup.html', {'error':'このユーザは既に登録されています'})
        user = User.objects.create_user(username_data, '', password_data)
    else:
        return render(request, 'signup.html', {})
    return render(request, 'signup.html', {})

def loginview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request, username=username_data, password=password_data)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')


def attendanceview(request):
    if request.method == 'POST':
        form = StaffAttendanceForm(request.POST or None)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = ChildCompanyModel.objects.get(id=obj.staff.id)
            obj.work_style = 0
            if "arrive" in request.POST:    # 出勤時
                obj.in_out = 0
                print("arrive")
            elif "leave" in request.POST:   # 退勤時
                obj.in_out = 1
                print("leave")
            obj.datetime = datetime.datetime.now()
            obj.save()

    template_name = "attendance.html"
    context = {"form": StaffAttendanceForm()}
    return render(request, template_name, context)


from django.http import HttpResponse
def sampleview(request):
    # staff = StaffModel.objects.all()      # 全件取得    
    staff = "Ichiro"                        # 将来的には受け取った名前を代入する
    day = datetime.datetime.today()         # 将来的には指定された範囲の日付から順に取得する

    # スタッフ名から定時と単価を取得
    regular_start_time =  StaffModel.objects.filter(name=staff).values_list("regular_start", flat=True)[0]
    regular_finish_time =  StaffModel.objects.filter(name=staff).values_list("regular_finish", flat=True)[0]
    ot_hourly_wage = StaffModel.objects.filter(name=staff).values_list("ot_wage", flat=True)[0]
    morning_hourly_wage = StaffModel.objects.filter(name=staff).values_list("morning_wage", flat=True)[0]

    # 定時を日付と結合してdatetime型に変更
    regular_start = datetime.datetime.combine(day, regular_start_time)
    regular_start = regular_start.astimezone(pytz.timezone('UTC'))
    regular_finish = datetime.datetime.combine(day, regular_finish_time)
    regular_finish = regular_finish.astimezone(pytz.timezone('UTC'))

    # 検索用
    start = datetime.datetime.combine(day, datetime.time(00,00,00))
    start = start.astimezone(pytz.timezone('UTC'))
    end = datetime.datetime.combine(day, datetime.time(23,59,59))
    end = end.astimezone(pytz.timezone('UTC'))

    # 勤怠データベースから該当する勤怠実績を取得 -> time型
    staff_arrive = AttendanceModel.objects.filter(in_out=0, attendance_datetime__gte=start, attendance_datetime__lte=end).values_list("attendance_datetime", flat=True)[0]      # 名前と日付で指定
    staff_leave = AttendanceModel.objects.filter(in_out=1, attendance_datetime__gte=start, attendance_datetime__lte=end).values_list("attendance_datetime", flat=True)[0]      # 名前と日付で指定

    print(staff_arrive.tzinfo)
    print(staff_leave.tzinfo)
    print(start.tzinfo)
    print(end.tzinfo)


    morning_wage = delta2chunk(regular_start - staff_arrive) * morning_hourly_wage
    ot_wage = delta2chunk(staff_leave - regular_finish) * ot_hourly_wage

    print("今日の残業手当は", str(morning_wage + ot_wage), "円です")
    return HttpResponse("sample")