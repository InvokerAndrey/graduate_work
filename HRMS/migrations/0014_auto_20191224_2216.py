# Generated by Django 3.0 on 2019-12-24 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS', '0013_auto_20191222_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='emotionality',
            field=models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='looseness',
            field=models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='self_centeredness',
            field=models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='smart',
            field=models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='sociability',
            field=models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True),
        ),
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sociability', models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True)),
                ('smart', models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True)),
                ('emotionality', models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True)),
                ('self_centeredness', models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True)),
                ('tension', models.DecimalField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (4, '5'), (4, '6'), (4, '7')], decimal_places=0, max_digits=3, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HRMS.Employee')),
            ],
        ),
    ]
