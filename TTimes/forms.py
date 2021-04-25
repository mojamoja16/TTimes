from django import forms
from django.forms import IntegerField, DateField, TimeField
from .models import StaffModel, AttendanceModel
import datetime

class StaffChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, staff):
        return f"{staff.name}"

class StaffAttendanceForm(forms.Form):
    class Meta:
        model = AttendanceModel

    staff = StaffChoiceField(
        queryset= StaffModel.objects.all(),
        empty_label= "choose...",
    )

    def save(self, in_out):
        attendance = AttendanceModel(
            staff = staff,
            company = company,
            work_style = 0,     # 将来的に日勤/夜勤用のボタンを実装
            in_out = in_out,
            date = datetime.date.today(),
            time = datetime.datetime.now()
        )
        self.save()