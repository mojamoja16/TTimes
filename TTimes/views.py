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
            return redirect('attendance')
        else:
            return redirect('login')
    return render(request, 'login.html')


def attendanceview(request):
    if request.method == 'POST':
        form = StaffAttendanceForm(request.POST or None)

        if form.is_valid():
            obj = form.save(commit=False)
            # obj.company = ChildCompanyModel.objects.get(id=obj.staff.id)    # staff.idが100とかになると子会社モデルでid=100が参照されエラーする
            obj.company = request.user  # ログイン機能を実装したらこっち
            obj.work_style = 0
            if "arrive" in request.POST:    # 出勤時
                obj.in_out = 0
                print("arrive")
            elif "leave" in request.POST:   # 退勤時
                obj.in_out = 1
                print("leave")
            obj.attendance_datetime = datetime.datetime.now()
            obj.save()
    
    print(str(request.user))
    print(type(request.user))
    template_name = "attendance.html"
    context = {"form": StaffAttendanceForm(user=request.user), "company": str(request.user)} ## StaffAttendanceFormにユーザー情報渡してます
    return render(request, template_name, context)


def staffpaymentview(request):
    company = request.user
    staffs = StaffModel.objects.filter(place=company).all()
    staff_list = {}
    for staff in staffs:
        staff_list[staff] = staffs.filter(name=staff).values()

    template_name = "staff_payment.html"
    context = {"staff_list": staff_list}
    return render(request, template_name, context)


from django.http import HttpResponse
def sampleview(request):
    # staff = StaffModel.objects.all()      # 全件取得    
    staff = "Ichiro"                        # 将来的には受け取った名前を代入する
    day = datetime.datetime.today()         # 将来的には指定された範囲の日付から順に取得する

    # スタッフ名から定時を取得
    REGULAR_START_TIME =  StaffModel.objects.filter(name=staff).values_list("regular_start", flat=True)[0]
    REGULAR_FINISH_TIME =  StaffModel.objects.filter(name=staff).values_list("regular_finish", flat=True)[0]

    # スタッフ名から勤務形態を取得
    OT_STYLE = StaffModel.objects.filter(name=staff).values_list("ot_style", flat=True)[0]
    MORNING_STYLE = StaffModel.objects.filter(name=staff).values_list("morning_style", flat=True)[0]
    NIGHT_STYLE = StaffModel.objects.filter(name=staff).values_list("night_style", flat=True)[0]
    HOLIDAY_STYLE = StaffModel.objects.filter(name=staff).values_list("holiday_style", flat=True)[0]
    
    # 定時を日付と結合してdatetime型に変更
    REGULAR_START = datetime.datetime.combine(day, REGULAR_START_TIME)
    REGULAR_START = REGULAR_START.astimezone(pytz.timezone('UTC'))
    REGULAR_FINISH = datetime.datetime.combine(day, REGULAR_FINISH_TIME)
    REGULAR_FINISH = REGULAR_FINISH.astimezone(pytz.timezone('UTC'))

    # 検索用の日時指定
    START = datetime.datetime.combine(day, datetime.time(00,00,00))
    START = START.astimezone(pytz.timezone('UTC'))
    END = datetime.datetime.combine(day, datetime.time(23,59,59))
    END = END.astimezone(pytz.timezone('UTC'))

    # 勤怠データベースから該当する勤怠実績を取得 -> time型
    staff_arrive = AttendanceModel.objects.filter(in_out=0, attendance_datetime__gte=START, attendance_datetime__lte=END).values_list("attendance_datetime", flat=True)[0]      # 名前と日付で指定
    staff_leave = AttendanceModel.objects.filter(in_out=1, attendance_datetime__gte=START, attendance_datetime__lte=END).values_list("attendance_datetime", flat=True)[0]      # 名前と日付で指定

    morning_delta = REGULAR_START - staff_arrive
    evening_delta = staff_leave - REGULAR_FINISH

    morning_wage, ot_wage = 0, 0        # 初期化

    # スタッフ名から単価を取得
    MORNING_HOURLY_WAGE = StaffModel.objects.filter(name=staff).values_list("morning_wage", flat=True)[0]
    OT_HOURLY_WAGE = StaffModel.objects.filter(name=staff).values_list("ot_wage", flat=True)[0]

    # 出勤時間と退勤時間が05:00または22:00を跨ぐか判断する関数
    # 8時間勤務を超えていないか判断する関数

    # 勤務形態と単価から手当を算出する関数
    def calc_payment(styl:int, wg:int, early:datetime.datetime, late:datetime.datetime):
        if styl == 0:       # 日当の場合
            return wg

        elif styl == 1:     # 時給の場合
            return delta2chunk(late-early) * wg
        
        else:               # 固定の場合
            return wg

    # 早出手当の算出





    if str(morning_delta.days).startswith("-"):
        # 遅刻した場合
        print("遅刻！")
        pass
    else:
        morning_wage = delta2chunk(morning_delta) * MORNING_HOURLY_WAGE
        
    if str(evening_delta.days).startswith("-"):
        # 早退した場合
        print("早退！")
        pass
    else:
        ot_wage = delta2chunk(evening_delta) * OT_HOURLY_WAGE
    
    print("今日の残業手当は", str(morning_wage + ot_wage), "円です")
    return HttpResponse("sample")