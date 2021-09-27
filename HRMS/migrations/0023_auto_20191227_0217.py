# Generated by Django 3.0 on 2019-12-26 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0022_auto_20191227_0207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirement',
            name='employee',
        ),
        migrations.AlterField(
            model_name='requirement',
            name='requirement_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Название требуемого навыка'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='value',
            field=models.DecimalField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], decimal_places=0, max_digits=5, null=True, verbose_name='Уровень владения требуемым навыком'),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirement_name', models.CharField(max_length=50, null=True, verbose_name='Название навыка')),
                ('value', models.DecimalField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7')], decimal_places=0, max_digits=5, null=True, verbose_name='Уровень владения навыком')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRMS.Employee')),
            ],
        ),
    ]
