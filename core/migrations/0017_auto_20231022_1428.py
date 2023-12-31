# Generated by Django 3.2.22 on 2023-10-22 13:28

import core.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=core.models.profile_image_file_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 14, 28, 2, 509683), verbose_name='date joined'),
        ),
    ]
