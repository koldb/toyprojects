# Generated by Django 4.0.4 on 2022-06-14 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_alter_newslist_rg_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newslist',
            name='time1',
        ),
        migrations.RemoveField(
            model_name='newslist',
            name='time2',
        ),
    ]