# Generated by Django 3.2.22 on 2023-10-20 09:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20231020_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 20, 10, 7, 38, 473667), verbose_name='date joined'),
        ),
    ]
