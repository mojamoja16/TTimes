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
        exclude = ['company', 'work_style', 'in_out', 'datetime']

    staff = StaffChoiceField(
        queryset= StaffModel.objects.filter()
        empty_label= "choose...",
    )