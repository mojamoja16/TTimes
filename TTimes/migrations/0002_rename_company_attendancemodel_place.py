# Generated by Django 3.2.2 on 2021-05-12 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TTimes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancemodel',
            old_name='company',
            new_name='place',
        ),
    ]