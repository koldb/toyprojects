from django.db import models

# Create your models here.


class User(models.Model):
    no = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, unique=True, verbose_name='아이디')
    user_pw = models.CharField(max_length=100, verbose_name='비밀번호')
    nickname = models.CharField(max_length=20, verbose_name='닉네임', null=True, blank=True)
    user_date = models.DateTimeField(auto_now_add=True)  # 입력시 현재 시간 날짜 삽입

    def __str__(self):
        return self.user_id

    class Meta:
        managed = True
        db_table = 'accounts'
        verbose_name = '유저'
        verbose_name_plural = '유저'