from django.db import models

# Create your models here.



class newsList(models.Model):
    id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=200, null=True, verbose_name='TITLE')
    news_url = models.CharField(max_length=100, null=True, verbose_name='URL')
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    lede = models.CharField(max_length=100, verbose_name='짧은 내용',  null=True, blank=True)
    writing = models.CharField(max_length=50, verbose_name='언론사', null=True, blank=True)
    comm = models.PositiveIntegerField(null=True, verbose_name='댓글 수')

    class Meta:
        managed = True
        db_table = 'news_lists'
        verbose_name = 'news'
        verbose_name_plural = 'news'


class news_comment(models.Model):
    no = models.AutoField(primary_key=True)
    rg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일자')
    register = models.CharField(max_length=30, verbose_name='작성자', null=True, blank=True)
    content = models.TextField(verbose_name='내용', null=True, blank=True)
    news_id = models.ForeignKey(newsList, on_delete=models.CASCADE, null=True, db_column="news_id")

    class Meta:
        managed = True
        db_table = 'news_comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'