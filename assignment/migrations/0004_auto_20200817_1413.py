# Generated by Django 3.1 on 2020-08-17 14:13

import assignment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_auto_20200817_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request_table',
            name='pincode',
            field=models.CharField(max_length=6, validators=[assignment.models.validate_pin], verbose_name='Pin Code'),
        ),
    ]
