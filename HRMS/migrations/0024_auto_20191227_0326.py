# Generated by Django 3.0 on 2019-12-27 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0023_auto_20191227_0217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='requirement_name',
            new_name='skill_name',
        ),
    ]
