from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, DetailView
from .models import *
from .forms import StaffAttendanceForm
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Define my function here.
import datetime
import pytz
import math
import csv
from io import TextIOWrapper, StringIO



def delta2chunk(delta: datetime.timedelta, chunk = 30):
    outlier = True                              # 遅刻/早退を管理するフラグ
    if delta < datetime.timedelta(days=0):
        # 遅刻/早退の場合は手当0
        quo = 0
        outlier = False
        return quo, outlier
    else:
        h, m, _ = str(delta).split(":")
        minutes = int(h) * 60 + int(m)
        quo = minutes // chunk
        if quo > 0:
            return quo, outlier
        else:
            return 0, outlier

# 検索の日時指定用.早朝5時締め．
def searchday(day:datetime.date):
    START = datetime.datetime.combine(day, datetime.time(5,00,00)).astimezone(pytz.timezone('UTC'))
    END = datetime.datetime.combine(day, datetime.time(4,59,59)).astimezone(pytz.timezone('UTC')) + datetime.timedelta(days=1)
    return (START, END)

def date_range(start, stop, step = timedelta(1)):
    current = start
    while current <= stop:
        yield current
        current += step


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
            return redirect('TTimes:attendance')
        else:
            return redirect('TTimes:login')
    return render(request, 'login.html')


class RegisterStaffView(CreateView):
    model = StaffModel
    fields = ["name", "email", "password", "place", "employee_number", "authority", "regular_start", "regular_finish", "day_break_start", "day_break_finish", "night_break_start", "night_break_finish", "ot_style", "morning_style", "night_style", "holiday_style", "ot_wage", "morning_wage", "night_wage", "holiday_wage", "rest_paid_holiday"]
    template_name = 'register_staff.html'

@login_required
def attendanceview(request):
    if request.method == 'POST':
        form = StaffAttendanceForm(request.user, request.POST or None)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.place = request.user
            obj.work_style = 0
            if "arrive" in request.POST:    # 出勤時
                obj.in_out = 0
                print("arrive")
            elif "leave" in request.POST:   # 退勤時
                obj.in_out = 1
                print("leave")
            obj.attendance_datetime = datetime.datetime.now()
            obj.save()
    
    template_name = "attendance.html"
    context = {"form": StaffAttendanceForm(user=request.user), "company": str(request.user)} ## StaffAttendanceFormにユーザー情報を渡す
    return render(request, template_name, context)

@login_required
def staffpaymentview(request):
    company = request.user
    staffs = StaffModel.objects.filter(place=company).all()
    staff_list = {}
    for staff in staffs:
        staff_list[staff] = staffs.filter(name=staff).values()

    template_name = "staff_payment.html"
    context = {
        "staff_list": staff_list,
        "company": str(request.user),
        }
    return render(request, template_name, context)

from .forms import SelectDateForm
@login_required
def dailylistview(request):
    if request.method == "POST":
        date = datetime.datetime.strptime(request.POST["date"], "%Y-%m-%d")
    else:
        date = datetime.datetime.today()
    company = request.user
    day_range = searchday(date) 
    # 出勤打刻時間から日勤/早出/夜勤/残業などを表示させる
    attendances = AttendanceModel.objects.filter(place=company, attendance_datetime__range=day_range)

    template_name = "attendance_list.html"

    context = {
        "attendances": attendances,
        "form": SelectDateForm(),
        "company": str(request.user),
    }
    return render(request, template_name, context)

@login_required
def staffrecordview(request, employee_number):
    if (request.method == "POST") and (request.POST["start"] != "") and (request.POST["end"] != "") :
        start_day = datetime.datetime.strptime(request.POST["start"], "%Y-%m-%d").astimezone(pytz.timezone('Asia/Tokyo'))
        end_day = datetime.datetime.strptime(request.POST["end"], "%Y-%m-%d").astimezone(pytz.timezone('Asia/Tokyo'))

        # 逆なら入れ替え
        if start_day > end_day:
            start_day, end_day = end_day, start_day
    else:

        # 締め日をとりあえず20として，21日で切り分けている．将来的にはモデルから引っ張ってくる．
        end_day = datetime.datetime.today().astimezone(pytz.timezone('Asia/Tokyo'))
        if end_day.day > 21:
            start_day = end_day.replace(day=21)
        else:
            start_day = end_day.replace(month=end_day.month-1, day=21)

    dates = date_range(start_day, end_day)
    company = request.user
    record_list = []

    staff_info = StaffModel.objects.filter(place=company, employee_number=employee_number)[0]
    staff = staff_info.name

    # スタッフ名から定時を取得
    REGULAR_START_TIME =  StaffModel.objects.filter(name=staff).values_list("regular_start", flat=True)[0]
    REGULAR_FINISH_TIME =  StaffModel.objects.filter(name=staff).values_list("regular_finish", flat=True)[0]

    # スタッフ名から勤務形態を取得
    OT_STYLE = StaffModel.objects.filter(name=staff).values_list("ot_style", flat=True)[0]
    MORNING_STYLE = StaffModel.objects.filter(name=staff).values_list("morning_style", flat=True)[0]
    NIGHT_STYLE = StaffModel.objects.filter(name=staff).values_list("night_style", flat=True)[0]
    HOLIDAY_STYLE = StaffModel.objects.filter(name=staff).values_list("holiday_style", flat=True)[0]

    # スタッフ名から単価を取得
    MORNING_WAGE_PER_UNIT_TIME = StaffModel.objects.filter(name=staff).values_list("morning_wage", flat=True)[0]
    OT_WAGE_PER_UNIT_TIME = StaffModel.objects.filter(name=staff).values_list("ot_wage", flat=True)[0]
    
    for date in dates:
        day_range = searchday(date)

        # 定時を日付と結合してdatetime型に変更
        REGULAR_START = datetime.datetime.combine(date, REGULAR_START_TIME).astimezone(pytz.timezone('UTC'))
        REGULAR_FINISH = datetime.datetime.combine(date, REGULAR_FINISH_TIME).astimezone(pytz.timezone('UTC'))
        
        # 初期化
        ARRIVE_SKIP_FLAG, LEAVE_SKIP_FLAG = False, False

        # 勤怠データベースから該当する勤怠実績を取得 -> time型のlist
        try:
            arrives = AttendanceModel.objects.filter(in_out=0, attendance_datetime__range=day_range, staff=staff_info.id).values_list("attendance_datetime", flat=True)
            # 出勤ボタンを二回以上押していた場合を回避する処理 最も早いものを採用
            if len(arrives) > 0:
                arrive = arrives[0]
            else:
                ARRIVE_SKIP_FLAG = True
                arrive = REGULAR_START
        
        except IndexError or AssertionError:   # 該当なしの場合なにエラーか分からんので適当
            # 勤怠修正画面に飛ばす
            pass

        try:
            lefts = AttendanceModel.objects.filter(in_out=1, attendance_datetime__range=day_range, staff=staff_info.id).values_list("attendance_datetime", flat=True)
            # 退勤ボタンを二回以上押していた場合を回避する処理 最も遅いものを採用
            if len(lefts) > 0:
                leave = lefts[len(lefts)-1]
            else:
                LEAVE_SKIP_FLAG = True
                leave = REGULAR_FINISH


        except IndexError or AssertionError:   # 該当なしの場合なにエラーか分からんので適当
            # 勤怠修正画面に飛ばす
            pass


        if  (len(arrives)* len(lefts) != 0 ) and (arrives[0] > lefts[0]):
            # 出勤/退勤ボタンを間違って押した時の処理 入れ替え操作
            arrive, leave = lefts[0], arrives[0]

        morning_delta = REGULAR_START - arrive
        evening_delta = leave - REGULAR_FINISH

        # 初期化
        morning_wage, ot_wage, night_wage, holiday_wage, status = 0, 0, 0, 0, ""
        
        morning_chunk, LATENESS_FLAG = delta2chunk(REGULAR_START - arrive)
        morning_wage = math.floor( morning_chunk * MORNING_WAGE_PER_UNIT_TIME / 2)
        if not LATENESS_FLAG:
            status += "遅刻"
        if morning_wage > 0:
            status += "早出"

        ot_chunk, EARLINESS_FLAG = delta2chunk(leave - REGULAR_FINISH)
        ot_wage = math.floor(ot_chunk * OT_WAGE_PER_UNIT_TIME / 2)
        if not EARLINESS_FLAG:
            status += "早退"
        if ot_wage > 0:
            status += "残業"
    
        if ARRIVE_SKIP_FLAG:
            arrive = "--:--"
        else:
            arrive = arrive.astimezone(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')

        if LEAVE_SKIP_FLAG:
            leave = "--:--"
        else:
            leave = leave.astimezone(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')

        sum = morning_wage + ot_wage + night_wage + holiday_wage

        if morning_wage == 0:
            morning_wage = "--"
        if ot_wage == 0:
            ot_wage = "--"
        if night_wage == 0:
            night_wage = "--"
        if holiday_wage == 0:
            holiday_wage = "--"

        record_list.append({
            "date": date.strftime('%m/%d') + f"({settings.DAY_MAP[date.strftime('%A')]})",
            "url_date":date.strftime("%Y-%m-%d"),
            "arrive": arrive,
            "leave": leave,
            "morning": str(morning_wage),
            "ot": str(ot_wage),
            "night": str(night_wage),
            "holiday": str(holiday_wage),
            "sum": sum,
            "status": status,
        })

    # 勤務形態と単価から手当を算出する関数
    def calc_payment(styl:int, wg:int, early:datetime.datetime, late:datetime.datetime):
        if styl == 0:       # 日当の場合
            return wg

        elif styl == 1:     # 時給の場合
            return delta2chunk(late-early)[0] * wg
        
        else:               # 固定の場合
            return wg
    
    template_name = "staff_record.html"

    context = {
        "staff_info": staff_info,
        "record_list":record_list,
        "form": SelectDateForm(), 
        "display_period": start_day.strftime('%m/%d') + " ~ " + end_day.strftime('%m/%d'), 
        "company": str(request.user),
    }

    return render(request, template_name, context)

@login_required
def manageattendanceview(request, pk):
    attendance = AttendanceModel.objects.get(pk=pk)
    print(attendance.staff.name, attendance.work_style, attendance.in_out, attendance.attendance_datetime)
    context = {"attendance": attendance}
    template_name = "attendance_manage.html"
    return render(request, template_name, context)


# csv読み込みテスト
@login_required
def uploadview(request):
    if 'uploaded_file' in request.FILES:
        if request.FILES['uploaded_file'].name.rsplit(".")[-1] not in ("csv", "CSV"):
            # csvファイルでなければ拒否する
            print("It does not support reading other than csv files")
        else:
            # utf-8で読み込み，データ登録
            form_data = TextIOWrapper(request.FILES['uploaded_file'].file, encoding='utf-8')
            csv_file = csv.reader(form_data)
            for line in csv_file:
                line = [el.translate(str.maketrans(settings.KILL_MULTIBYTE_MAP)) for el in line ]
                try:
                    _ , created = StaffModel.objects.get_or_create(
                        name = line[0],
                        place = request.user,
                        employee_number = line[1],
                        authority = line[2],
                        regular_start = line[3],
                        regular_finish = line[4],
                        day_break_start = line[5],
                        day_break_finish = line[6],
                        night_break_start = line[7],
                        night_break_finish = line[8],
                        ot_style = line[9],
                        morning_style = line[10],
                        night_style = line[11],
                        holiday_style = line[12],
                        ot_wage = line[13],
                        morning_wage = line[14],
                        night_wage = line[15],
                        holiday_wage = line[16],
                        rest_paid_holiday = line[17],
                        )
                    # 既存等の理由で作成されなかったレコードは名前をピックアップ
                    if not created:
                        print(f"{line[0]} has already been registered, thus skipped.")

                except ValueError:
                    print(f"Error occued at {line[0]}'s row. Please validate the datas.")

    return render(request, 'upload.html')

from django.http import HttpResponse
@login_required
def downloadview(request):
    # レスポンスの設定
    response = HttpResponse(content_type='text/csv')
    filename = 'data.csv'  # ダウンロードするcsvファイル名
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    writer = csv.writer(response)

    # 1行目にヘッダーを書き込む 文字化けする～～エンコード指定方法調べる
    header = ['氏名','勤務先','残有休']
    writer.writerow(header)
    # データ出力
    staffs = StaffModel.objects.filter(place=request.user)
    for staff in staffs:
        writer.writerow([staff.name, staff.place, staff.rest_paid_holiday])
    return response