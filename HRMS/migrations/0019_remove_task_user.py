# Generated by Django 3.0 on 2019-12-14 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0018_auto_20191214_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]