# Generated by Django 3.0 on 2019-12-08 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0006_auto_20191208_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
    ]