# Generated by Django 4.0.4 on 2022-05-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='newsList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('news_title', models.CharField(max_length=200, null=True, verbose_name='TITLE')),
                ('news_url', models.CharField(max_length=100, null=True, verbose_name='URL')),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('comm', models.PositiveIntegerField(null=True, verbose_name='댓글 수')),
            ],
            options={
                'verbose_name': 'news',
                'verbose_name_plural': 'news',
                'db_table': 'news_lists',
                'managed': True,
            },
        ),
    ]
