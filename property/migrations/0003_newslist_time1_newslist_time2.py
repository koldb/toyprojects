# Generated by Django 4.0.4 on 2022-05-25 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_newslist_lede'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslist',
            name='time1',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='시간 1'),
        ),
        migrations.AddField(
            model_name='newslist',
            name='time2',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='시간 2'),
        ),
    ]
