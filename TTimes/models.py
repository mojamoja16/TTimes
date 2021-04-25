from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ParentCompanyModel(models.Model):
    class Meta:
        verbose_name_plural = "親会社モデル"
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ChildCompanyModel(models.Model):
    class Meta:
        verbose_name_plural = "子会社モデル"
    name = models.CharField(max_length=100)
    parent_company= models.ForeignKey(ParentCompanyModel, on_delete=models.CASCADE, verbose_name='親会社', default=None)
    def __str__(self):
        return self.parent_company.name + " -- " + self.name

AUTH_LEVEL = [(0, '一般職'), (1, '管理職')]
PAY_STYLE = [(0, '日当'), (1, '時給'), (2, '固定')]
class StaffModel(models.Model):
    class Meta:
        verbose_name_plural = "従業員モデル"
    name = models.CharField(verbose_name="氏名", max_length=100)
    place = models.ForeignKey(ChildCompanyModel, on_delete=models.CASCADE, verbose_name='勤務先', default=None)
    employee_number = models.IntegerField(verbose_name='社員番号', default=None)
    authority = models.IntegerField(verbose_name='職位',choices=AUTH_LEVEL, default=0)
    

    regular_start = models.TimeField(verbose_name="始業時間")
    regular_finish = models.TimeField(verbose_name="終業時間")
    day_break_start = models.TimeField(verbose_name="休憩開始時間")
    day_break_finish = models.TimeField(verbose_name="休憩終了時間")
    night_break_start = models.TimeField(verbose_name="(夜)休憩開始時間")
    night_break_finish = models.TimeField(verbose_name="(夜)休憩終了時間")

    ot_style = models.IntegerField(verbose_name='残業形態',choices=PAY_STYLE, default=1)
    morning_style = models.IntegerField(verbose_name='早出形態',choices=PAY_STYLE, default=1)
    night_style = models.IntegerField(verbose_name='夜勤形態',choices=PAY_STYLE, default=2)
    holiday_style = models.IntegerField(verbose_name='休出形態',choices=PAY_STYLE, default=0)
    ot_wage = models.IntegerField(verbose_name='残業単価', default=None)
    morning_wage = models.IntegerField(verbose_name='早出単価', default=None)
    night_wage = models.IntegerField(verbose_name='夜勤単価', default=None)
    holiday_wage = models.IntegerField(verbose_name='休出単価', default=None)
    rest_paid_holiday = models.IntegerField(verbose_name='残有休', default=None)

    def __str__(self):
        return self.name + " -- " + str(self.place.name)

WORK_STYLE = [(0, '日勤'), (1, '夜勤')]
IN_OUT = [(0, '出勤'), (1, '退勤')]
class AttendanceModel(models.Model):
    class Meta:
        verbose_name_plural = "勤怠モデル"

    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, related_name="staff")
    company = models.ForeignKey(ChildCompanyModel, verbose_name='勤務先', on_delete=models.CASCADE)
    work_style = models.IntegerField(verbose_name='日勤/夜勤', choices=WORK_STYLE, default=0)
    in_out = models.IntegerField(verbose_name='出勤/退勤', choices=IN_OUT)
    date = models.DateField(verbose_name='打刻日')
    time = models.TimeField(verbose_name="打刻時間")
    
    corrector = models.ForeignKey(StaffModel, on_delete=models.CASCADE, related_name="corrector", null=True, blank=True)
    arrive_correct = models.TimeField(verbose_name="(修正)出社時間", null=True, blank=True)
    leave_correct = models.TimeField(verbose_name="(修正)退社時間", null=True, blank=True)

    def __str__(self):
        return str(self.staff.name) +" "+ str(self.company.name) +" "+ str(self.date) +" "+ str(self.time)
