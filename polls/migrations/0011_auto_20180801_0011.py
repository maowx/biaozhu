# Generated by Django 2.0.7 on 2018-07-31 16:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20180801_0009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pool',
            old_name='pic',
            new_name='picture',
        ),
        migrations.AlterField(
            model_name='choice',
            name='choose_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 31, 16, 11, 53, 108707, tzinfo=utc)),
        ),
    ]
