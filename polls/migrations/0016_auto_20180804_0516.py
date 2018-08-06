# Generated by Django 2.0.7 on 2018-08-04 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_auto_20180803_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='user_id',
        ),
        migrations.AddField(
            model_name='choice',
            name='user',
            field=models.ForeignKey(choices=[(1, 'mwx'), (2, 'mao')], default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, to='polls.User', verbose_name='标注人员'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_num',
            field=models.IntegerField(choices=[(1, '左图更优'), (2, '右图更优'), (3, '两图相似')], editable=False, verbose_name='选择图片'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='left_pic_id',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='choice',
            name='right_pic_id',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='choice',
            name='use_time',
            field=models.IntegerField(editable=False, verbose_name='使用时间'),
        ),
        migrations.AlterField(
            model_name='pool',
            name='group',
            field=models.ForeignKey(choices=[(1, 'a'), (2, 'b'), (3, 'c')], on_delete=django.db.models.deletion.CASCADE, to='polls.Group', verbose_name='标签'),
        ),
    ]
