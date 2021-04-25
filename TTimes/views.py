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
        # request.POSTから打刻者のStaffModelにおけるidを取得
        staff_id = int(request.POST["staff"])
        # StaffModelから打刻者の名前を取得
        staff_name = StaffModel.objects.get(pk=staff_id)
        # StaffModelから打刻者の勤務先を取得
        staff_company_id = StaffModel.objects.filter(name=staff_name).values_list("place", flat=True)
        # 勤務先の名前からChildCompanyModelにおけるidを取得し，代入（将来的にはログインしている会社を選択する）
        company = ChildCompanyModel.objects.get(pk=staff_company_id)
        work_style = 0
        # 将来的にはボタンを複数用意して取得するなど

        if "arrive" in request.POST:    # 出勤時
            in_out = 0
        elif "leave" in request.POST:   # 退勤時
            in_out = 1

        attendance = AttendanceModel.objects.create(
            staff=staff_name,
            company=company,
            work_style=work_style,
            in_out=in_out,
            date=datetime.date.today(),
            time=datetime.datetime.now().time()
            )

    template_name = "attendance.html"
    context = {"form": StaffAttendanceForm()}
    return render(request, template_name, context)


from django.http import HttpResponse
def sampleview(request):
    # staff = StaffModel.objects.all()      # 全件取得    
    staff = "Ichiro"                        # 将来的には受け取った名前を代入する
    day = datetime.date(2021, 4, 16)        # 将来的には指定された範囲の日付から順に取得する

    # スタッフ名から定時と単価を取得
    regular_start_time =  StaffModel.objects.filter(name=staff).values_list("regular_start", flat=True)[0]
    regular_finish_time =  StaffModel.objects.filter(name=staff).values_list("regular_finish", flat=True)[0]
    ot_hourly_wage = StaffModel.objects.filter(name=staff).values_list("ot_wage", flat=True)[0]
    morning_hourly_wage = StaffModel.objects.filter(name=staff).values_list("morning_wage", flat=True)[0]

    # 定時を日付と結合してdatetime型に変更
    regular_start = datetime.datetime.combine(day, regular_start_time)
    regular_finish = datetime.datetime.combine(day, regular_finish_time)

    # 勤怠データベースから該当する勤怠実績を取得 -> time型
    staff_arrive_time = AttendanceModel.objects.filter(in_out=0, date=day).values_list("time", flat=True)[0]      # 名前と日付で指定
    staff_leave_time = AttendanceModel.objects.filter(in_out=1, date=day).values_list("time", flat=True)[0]      # 名前と日付で指定

    print(staff_arrive_time)
    print(staff_leave_time)

    # 勤怠実績をtime型からdatetime型に
    staff_arrive = datetime.datetime.combine(day, staff_arrive_time)
    staff_leave = datetime.datetime.combine(day, staff_leave_time)

    morning_wage = delta2chunk(regular_start - staff_arrive) * morning_hourly_wage
    ot_wage = delta2chunk(staff_leave - regular_finish) * ot_hourly_wage

    print("今日の残業手当は", str(morning_wage + ot_wage), "円です")
    return HttpResponse('sample')