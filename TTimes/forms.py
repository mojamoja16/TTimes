from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.forms import IntegerField, DateField, TimeField
from .models import StaffModel, AttendanceModel
import datetime

class StaffChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, staff):
        return f"{staff.name}"

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceModel
        fields = ['staff',]
        exclude = ['place', 'work_style', 'in_out', 'datetime']
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ## viewから持ってきたuser変数をもとに該当フィールドに表示するデータを制限
        self.fields['staff'].queryset = StaffModel.objects.filter(place=user)
        
    staff = StaffChoiceField( ## ここはtemplate側で表示する名前を制限しているのに使っているので残す
        queryset= StaffModel.objects.all(),
        empty_label= "choose...",
    )

class SelectDateForm(forms.Form):
    date = forms.DateField(
        widget=DatePickerInput(format='%Y-%m-%d')
    )