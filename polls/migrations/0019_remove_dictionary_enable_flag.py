# Generated by Django 2.0.7 on 2018-08-04 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20180804_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictionary',
            name='enable_flag',
        ),
    ]
