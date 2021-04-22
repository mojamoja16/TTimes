from django import forms
from .models import StaffModel

class StaffAttendanceForm(forms.Form):
#     staff_id = forms.IntegerField()
    choices = [(staff.id, staff.name) for staff in StaffModel.objects.all()]

    staff_name = forms.ChoiceField(choices= choices, initial= ("", "sample"))

# from .models import SubmitAttendance

# class SubmitAttendanceForm(forms.ModelForm):
# 
#     class Meta:
#         model = SubmitAttendance
#         fields = ('place', 'in_out')