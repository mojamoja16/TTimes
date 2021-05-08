from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import uuid as uuid_lib
from datetime import datetime, timedelta
import pytz

# Create your models here. 
# コピペ
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not name:
            raise ValueError('Users must have an name')
        elif not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            name = name,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(
            name,
            email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class ParentCompanyModel(models.Model):
    class Meta:
        verbose_name_plural = "親会社モデル"
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class ChildCompanyModel(AbstractBaseUser, PermissionsMixin):
    # ユーザー AbstractUserをコピペし編集

    name = models.CharField(
        _('会社名'),
        max_length=100,
        unique=True,
        help_text=_(
            'Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists.  "),
            },
        )
    email = models.EmailField(
        max_length=255,
        unique=False,
        )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
        )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
            ),
        )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    parent_company= models.ForeignKey(ParentCompanyModel, on_delete=models.CASCADE, verbose_name='親会社', default='', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('子会社モデル')
        verbose_name_plural = _('子会社モデル')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Send an email to this user.
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    # # 既存メソッドの変更
    # def get_full_name(self):
    #     return self.full_name

    # def get_short_name(self):
    #     return self.full_name

    def __str__(self):
        return self.name


"""
class ChildCompanyModel(models.Model):
    class Meta:
        verbose_name_plural = "子会社モデル"
    name = models.CharField(max_length=100)
    parent_company= models.ForeignKey(ParentCompanyModel, on_delete=models.CASCADE, verbose_name='親会社', default=None)
    def __str__(self):
        return self.parent_company.name + " -- " + self.name
"""

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
    attendance_datetime = models.DateTimeField(verbose_name='打刻日時')

    
    corrector = models.ForeignKey(StaffModel, on_delete=models.CASCADE, related_name="修正者", null=True, blank=True)
    arrive_correct = models.TimeField(verbose_name="(修正)出社時間", null=True, blank=True)
    leave_correct = models.TimeField(verbose_name="(修正)退社時間", null=True, blank=True)
    correct_reason = models.CharField(verbose_name="修正理由・備考", max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.staff.name) +" "+ str(self.company.name) +" "+ str(self.attendance_datetime.astimezone(pytz.timezone('Asia/Tokyo')))[:-6]