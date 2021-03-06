# Generated by Django 3.0 on 2019-12-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0005_auto_20191221_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='course',
            field=models.CharField(choices=[('Нет', 'Нет'), ('Программирование', 'Программирование'), ('Тестирование', 'Тестирование'), ('Системное администрирование', 'Системное администрирование'), ('SAP', 'SAP')], max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='foreign_language',
            field=models.CharField(choices=[('Нет', 'Нет'), ('Английский', 'Английский'), ('Немецкий', 'Немецкий'), ('Испанский', 'Испанский'), ('Китайский', 'Китайский'), ('Французский', 'Французский')], max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='language_level',
            field=models.CharField(blank=True, choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='education_type',
            field=models.CharField(choices=[('Высшее образование', 'Высшее образование'), ('Среднее образование', 'Среднее образование')], max_length=100, null=True),
        ),
    ]
