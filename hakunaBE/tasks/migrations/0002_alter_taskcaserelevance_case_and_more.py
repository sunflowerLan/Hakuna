# Generated by Django 4.0.3 on 2022-07-01 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcaserelevance',
            name='case',
            field=models.TextField(default='', null=True, verbose_name='关联用例'),
        ),
        migrations.AlterField(
            model_name='testtask',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
