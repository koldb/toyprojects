# Generated by Django 4.0.4 on 2022-05-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_news_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslist',
            name='writing',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='언론사'),
        ),
    ]