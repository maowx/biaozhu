# Generated by Django 2.0.7 on 2018-08-03 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20180801_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[(0, '正常'), (1, '已拉黑')], default=0, editable=False, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice_num',
            field=models.IntegerField(choices=[(1, '左图更优'), (2, '右图更优'), (3, '两图相似')], verbose_name='选择图片'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choose_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='操作时间'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='use_time',
            field=models.IntegerField(verbose_name='使用时间'),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(max_length=200, verbose_name='标签名称'),
        ),
        migrations.AlterField(
            model_name='pool',
            name='picture',
            field=models.ImageField(upload_to='img', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='pool',
            name='title',
            field=models.CharField(max_length=200, verbose_name='标题'),
        ),
    ]
