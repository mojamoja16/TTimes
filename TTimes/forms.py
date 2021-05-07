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
        fields = ['staff', 'company', 'work_style', 'in_out', 'datetime']

    staff = StaffChoiceField(
        queryset= StaffModel.objects.all(),
        empty_label= "choose...",
    )
    