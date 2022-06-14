from django.shortcuts import render, redirect, get_object_or_404
import requests
import urllib.request as req

from pandas import DataFrame
from bs4 import BeautifulSoup, Comment
from datetime import datetime
import os
from .models import newsList, news_comment
from django.core.paginator import Paginator
import datetime
from datetime import date
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.urls import reverse
from .decorators import login_required
import re


def index(request):
    nickname = request.session.get('nickname')

    url = "https://finance.naver.com/marketindex/"

    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser", from_encoding='euc-kr')

    name_nation = soup.select('h3.h_lst > span.blind')
    name_price = soup.select('span.value')

    nlist = {}
    i = 0
    for c_list in soup:
        try:

            nlist[i] = {'ntitle': name_nation[i].text, 'nnum': name_price[i].text}

            i = i + 1
        except IndexError:
            pass

    flist = nlist.values()
    context = {'nickname': nickname, 'flist': flist}
    return render(request, 'property/index.html', context)


# 엑셀 저장
def naver_excel(request):
    # naver finance 인기 검색 종목
    print('크롤링 시작')

    date = str(datetime.now())
    date_str = date.split()[0].replace('-', '')
    date = date[:date.rfind(':')].replace(' ', '_')
    date = date.replace(':', '시') + '분'

    urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=260'
    header = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(urls, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')

    # main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-child(1) > dl > dt:nth-child(2) > a

    news_dict = {}
    idx = 0
    cur_page = 1
    print('크롤링 중...')

    pages = soup.find('div', {'class': 'paging'})

    while True:
        main = soup.find('div', {'class': 'list_body newsflash_body'})

        li_list = main.find_all('dl')

        area_list = [li.find('dt') for li in li_list]
        # 사진없는 기사 포함된 경우 오류발생
        # area_list = [li.find('dt', {'class' : 'photo'}) for li in li_list]
        a_list = [area.find('a') for area in area_list]

        for n in a_list[:len(a_list)]:
            try:
                news_dict[idx] = {'title': n.find('img').get('alt').strip(), 'url': n.get('href')}
            except:
                news_dict[idx] = {'title': n.text.strip(), 'url': n.get('href')}
            idx += 1

        if cur_page < len(pages.find_all('a')) + 1:
            try:
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print("찐 왓다감")
            except:
                next_page_url = [p for p in pages.find_all('a') if p.text == '다음'][0].get('href')
                cur_page = 11
        elif cur_page > len(pages.find_all('a')) + 1:
            try:
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print("찐 왓다감")
            except:
                break
        elif cur_page == 40:
            break
        req = requests.get('https://news.naver.com/main/list.naver' + next_page_url, headers=header)
        soup = BeautifulSoup(req.text, 'html.parser')
        pages = soup.find('div', {'class': 'paging'})

        cur_page += 1

    print('크롤링 완료')

    news_df = DataFrame(news_dict).T

    folder_path = os.getcwd()

    xlsx_file_name = '네이버뉴스_{}.xlsx'.format(date)
    news_df.to_excel(xlsx_file_name, index=None, encoding='euc-kr')

    # context = {'news_dict': news_dict}

    return render(request, 'property/newsView.html')

    # print(news_df['title'])
    # print(news_df.iloc[:10])


# 크롤링 불러오기
@login_required
def naver_news_insert(request):
    print('크롤링 시작')

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
        global time1
        global time2
        time1 = None
        time2 = None


        print(len(pages.find_all('a')))
        print('cur : ', cur_page)
        if cur_page == len(pages.find_all('a')):
            try:
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print('cur 작다 try : ', next_page_url)
            except:
                print('cur 동일 브레이크')
                break
        elif 0 <= cur_page < len(pages.find_all('a')):
            try:
                next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page + 1)][0].get('href')
                print('cur 크다 try : ', next_page_url)
            except:
                next_page_url = [p for p in pages.find_all('a') if p.text == '이전'][0].get('href')
                print('cur 작다 except : ', next_page_url)
        elif cur_page == -1:
            print('cur = 0 끝')
            break

        req = requests.get('https://news.naver.com/main/list.naver' + next_page_url, headers=header)
        soup = BeautifulSoup(req.text, 'html.parser')
        pages = soup.find('div', {'class': 'paging'})

        cur_page -= 1

        main = soup.find('div', {'class': 'list_body newsflash_body'})

        li_list2 = main.find_all('dl')

        for n in li_list2:
            news_title = n.find('a').text.strip()

            if news_title != "":
                news_title = n.find('a').text.strip()
                news_url = n.find('a').get('href')
                lede = n.find('span').text.strip()
                writing = n.find('span', {'class': 'writing'})
                time_1 = n.find('span', {'class': 'date is_new'})
                time_2 = n.find('span', {'class': 'date is_outdated'})
                if time_1 == None:
                    time2 = re.sub(r'[^0-9]','',time_2.text.strip())
                    #print('title 있음 time2: ', re.sub(r'[^0-9]','',time2))
                else:
                    time1 = re.sub(r'[^0-9]','',time_1.text.strip())
                    #print('title 있음  time1: ', re.sub(r'[^0-9]','',time1))

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
                time_1 = n.find('span', {'class': 'date is_new'})
                time_2 = n.find('span', {'class': 'date is_outdated'})
                if time_1 == None:
                    time2 = re.sub(r'[^0-9]','',time_2.text.strip())
                    #print('title 사진 time2: ', re.sub(r'[^0-9]','',time2))
                else:
                    time1 = re.sub(r'[^0-9]','',time_1.text.strip())
                    #print('title 사진  time1: ', re.sub(r'[^0-9]','',time1))

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
                    writing=writing,
                    time1=time1,
                    time2=time2
                ).save()
            else:
                old = get_object_or_404(newsList, news_url=news_url)
                old.time1 = time1
                old.time2 = time2
                old.save()
    return redirect('property:naver_list')


# 네이버 리스트
@login_required
def naver_list(request):
    # 리스트 불러오기
    nickname = request.session.get('nickname')
    # nlist = newsList.objects.filter(rg_date__gte=date.today()).order_by('rg_date')
    # 검색 추가
    sort = request.GET.get('sort', '')
    query = request.GET.get('q', '')
    print(query)
    if sort == 'news_title':
        nlist = newsList.objects.filter(Q(news_title__icontains=query), rg_date__gte=date.today()).order_by('rg_date')
    elif sort == 'writing':
        nlist = newsList.objects.filter(Q(writing__icontains=query), rg_date__gte=date.today()).order_by('rg_date')
    else:
        print('리스트')
        nlist = newsList.objects.filter(rg_date__gte=date.today()).order_by('-rg_date')

    page = request.GET.get('page', '1')
    paginator = Paginator(nlist, 20)
    page_obj = paginator.get_page(page)
    context = {'page_obj': page_obj, 'nickname': nickname, 'sort': sort, 'query': query}
    print('리스트 완료')
    return render(request, 'property/news_list.html', context)


# 네이버 뉴스 뷰
def naver_view(request, pk):
    nickname = request.session.get('nickname')
    # 저장된 내용 불러오기
    detail_news = get_object_or_404(newsList, id=pk)
    comments = news_comment.objects.filter(news_id=pk).order_by('rg_date')
    print('url 불러오기 : ', detail_news.news_url)

    # 들어가면서 본문 내용 가져오기
    urls = detail_news.news_url
    header = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(urls, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')

    main = soup.find('div', {'class': 'go_trans _article_content'})


    for x in main.find_all("br"):
        print('1번쨰 : ', x)
        x.replace_with("\n")
        print('1번쨰 끝 : ', x)

    #
    # main_con = "".join([str(x) for x in main.contents])  # 최상위 태그 제거(=innerHtml 추출)
    # text = main_con.strip()

    text = main.text.strip()

    print(text)
    context = {'detail_news': detail_news, 'text': text, 'nickname': nickname, 'comments': comments}
    return render(request, 'property/news_view.html', context)


# 댓글/대댓글
def comment_create(request, pk):
    comment_count = news_comment.objects.filter(news_id=pk).count() + 1
    newscomm = get_object_or_404(newsList, id=pk)
    print("댓글 시작")
    if request.method == 'POST':
        print("댓글 저장")
        comment = news_comment()
        comment.register = request.POST.get('register')
        comment.content = request.POST.get('content')
        comment.news_id_id = pk
        comment.save()

        print('댓글수 저장')
        newscomm.comm = comment_count
        newscomm.save()
        # return render(request, 'question/que_detail.html', {'detailView': que_sheet, 'comments': comments, 'login_session': login_session})
        return HttpResponseRedirect(reverse('property:naver_view', args=[pk]))
    else:
        print('GET 들어옴 / 댓글 조회')


# 댓글 삭제
def com_delete(request, no, qno):
    print("댓글 삭제 시작")
    comments = news_comment.objects.filter(no=qno)
    comments.delete()

    comment_count = news_comment.objects.filter(news_id=no).count()
    newscomm = get_object_or_404(newsList, id=no)
    newscomm.comm = comment_count
    print(newscomm.comm)
    newscomm.save()

    print('댓글 삭제 완료')
    return redirect('question:que_detail', no)


# 댓글 수정
def comment_modify(request):
    print('댓글 수정 시작')
    jsonObject = json.loads(request.body)
    comment = news_comment.objects.filter(no=jsonObject.get('no'))
    context = {
        'result': 'no'
    }
    if comment is not None:
        print('업데이트 시작')
        comment.update(content=jsonObject.get('content'))
        context = {
            'result': 'ok'
        }
        print('댓글 수정 성공')
        return JsonResponse(context);
    return JsonResponse(context)
