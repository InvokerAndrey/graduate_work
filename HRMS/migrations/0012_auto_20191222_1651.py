# Generated by Django 3.0 on 2019-12-22 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0011_auto_20191221_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='education_required',
            field=models.DecimalField(choices=[(0, 'Образование не требуется'), (1, 'Среднее образование'), (2, 'Высшее образование')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='experience_required',
            field=models.DecimalField(choices=[(0, 'Опыт работы не требуется'), (1, '1 год'), (2, '2 года'), (3, '3 года'), (4, '4 года'), (5, '5 и более лет')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='language_level',
            field=models.DecimalField(blank=True, choices=[(1, 'A1'), (2, 'A2'), (3, 'B1'), (4, 'B2'), (5, 'C1'), (6, 'C2')], decimal_places=0, max_digits=3, null=True),
        ),
    ]
