import sys

sys.path.append('../..')
#app 없이 외부에서 실행시 필요한 코드(하단 8번째 줄까지)
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from property.models import newsList, news_comment
from django.shortcuts import render, redirect, get_object_or_404
import requests
import urllib.request as req
import os


from pandas import DataFrame
from bs4 import BeautifulSoup, Comment
from datetime import datetime

from django.core.paginator import Paginator
import datetime
from datetime import date
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.urls import reverse
from property.decorators import login_required
import re

def naver_news_insert():
    print('크롤링 시작 => ', datetime.now())

    urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=260'
    header = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(urls, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')


    print('크롤링 중...')

    pages = soup.find('div', {'class': 'paging'})
    #cur_page = 1
    cur_page = len(pages.find_all('a'))

    # cur_page = len(pages.find_all('a')) + 1
    # news = newsList.objects.all()

    # newslists = newsList.objects.all()
    while True:

        # cur_page <= (len(pages.find_all('a')) + 1):
        main = soup.find('div', {'class': 'list_body newsflash_body'})

        li_list = main.find_all('dl')

        area_list = [li.find('dt') for li in li_list]
        dd_list = [li.find('dd') for li in li_list]
        # 사진없는 기사 포함된 경우 오류발생
        # area_list = [li.find('dt', {'class' : 'photo'}) for li in li_list]
        a_list = [area.find('a') for area in area_list]
        span_list = [area.find('span') for area in dd_list]


        print(len(pages.find_all('a')))
        print('cur : ', cur_page)
        #if cur_page == len(pages.find_all('a')):
        if 10 <= cur_page < len(pages.find_all('a')):
            try:
                print('cur 동일 ')
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print(next_page_url)
                cur_page += 1
            except:
                next_page_url = [p for p in pages.find_all('a') if p.text == '다음'][0].get('href')
                print('cur 작다 try : ', next_page_url)
                cur_page += 1
        elif cur_page == 10:
                next_page_url = [p for p in pages.find_all('a') if p.text == '다음'][0].get('href')
                print('cur 작다 try : ', next_page_url)
                cur_page += 1

        elif 0 <= cur_page < 10:
            try:
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print('cur 크다 try : ', next_page_url)
                cur_page -= 1
            except:
                next_page_url = [p for p in pages.find_all('a') if p.text == '이전'][0].get('href')
                print('cur 작다 except : ', next_page_url)
                cur_page -= 1
        elif cur_page > len(pages.find_all('a')):
            try:
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print('cur 크다2 try ', next_page_url)
                cur_page += 1
            except:
                cur_page = 9
        elif cur_page == -1:
            print('cur = 0 끝')
            break

        req = requests.get('https://news.naver.com/main/list.naver' + next_page_url, headers=header)
        soup = BeautifulSoup(req.text, 'html.parser')
        pages = soup.find('div', {'class': 'paging'})



        main = soup.find('div', {'class': 'list_body newsflash_body'})

        li_list2 = main.find_all('dl')

        for n in li_list2:
            news_title = n.find('a').text.strip()

            if news_title != "":
                news_title = n.find('a').text.strip()
                news_url = n.find('a').get('href')
                lede = n.find('span').text.strip()
                writing = n.find('span', {'class': 'writing'})
                if writing == None:
                    print('title 있음 pass')
                    pass
                else:
                    writing = writing.text.strip()
            else:
                news_title = n.find('img').get('alt').strip()
                news_url = n.find('a').get('href')
                lede = n.find('span').text.strip()
                writing = n.find('span', {'class': 'writing'})
                if writing == None:
                    print('title 사진 pass')
                    pass
                else:
                    writing = writing.text.strip()
            news = newsList.objects.filter(news_url=news_url).order_by('-rg_date')
            if news.count() == 0:
                # print('중복확인 저장 시작')
                newsList(
                    news_title=news_title,
                    news_url=news_url,
                    lede=lede,
                    writing=writing
                ).save()



naver_news_insert()