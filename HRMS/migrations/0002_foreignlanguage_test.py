# Generated by Django 3.0 on 2019-12-20 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreignlanguage',
            name='test',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
