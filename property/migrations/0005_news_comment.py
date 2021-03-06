# Generated by Django 4.0.4 on 2022-05-26 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_newslist_rg_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='news_comment',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('rg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록일자')),
                ('register', models.CharField(blank=True, max_length=30, null=True, verbose_name='작성자')),
                ('content', models.TextField(blank=True, null=True, verbose_name='내용')),
                ('news_id', models.ForeignKey(db_column='news_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='property.newslist')),
            ],
            options={
                'verbose_name': '댓글',
                'verbose_name_plural': '댓글',
                'db_table': 'news_comment',
                'managed': True,
            },
        ),
    ]
