from urllib import parse
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
import time
import re
from settings import WEB_DRIVER_PATH, XLSX_PATH

start = '20170305'
end = '20170405'
keyword = '나노하나'
def make_basic_url(keyword, start, end):
    base_url = 'https://m.search.naver.com/search.naver?display=15&nso=p%3A'
    period = 'from' + start + 'to' + end
    query = '&query=' + parse.quote(keyword)
    end = '&where=m_blog&start='
    final_url = base_url + period + query + end
    return final_url

basic_url = make_basic_url(keyword, start, end)
blog_postings = get_blog_posting_urls()

def get_blog_posting_urls(blog_postings):
    index = 1
    flag = True
    driver = webdriver.Chrome(WEB_DRIVER_PATH)
    regex_href = r'.*https:\/\/m\.blog\.naver\.com\/(\w*\/\d*)'
    while(index < 15):
        # index에 해당하는 url
        url = basic_url + str(index)

        driver.get(url)
        html = driver.page_source
        bs = BeautifulSoup(html, 'html5lib')
        links = bs.select('.bx a')
        for single_link in links:
        # single_link가 https://m.blg.naver.com을 포함하면 그걸 가져오자
            href = re.findall(regex_href, str(single_link))
            if href != None and href !=[]:
                if href in blog_postings:
                    flag = False
                    break;
                else:
                    blog_postings.append(href)
        index += 15
    return blog_postings

# link를 돌면서 제목, 본문, 날짜 넣기
blog_base_url = 'https://m.blog.naver.com/'
titles = []
texts = []
dates = []

for posting_addr in blog_postings:
    posting_addr = str(posting_addr).strip('[]')
    posting_addr = posting_addr.strip('\'\'')
    url = blog_base_url + posting_addr
    get_element(url)

DATE = 0
TITLE = 1
TEXT = 2

def get_element(url):
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    date = get_element(bs, DATE)
    dates.append(date)

    title = get_element(bs, TITLE)
    titles.append(title)

    text = get_element(bs, TEXT)
    texts.append(text)

def get_element(bs, type):
    switcher = {
        0: get_date,
        1: get_title,
        2: get_text
    }
    switcher.get(type)(bs)


def get_date(bs):
    date_divs = bs.select('.se_date')
    date = re.findall(r'(20[\d\s\.\:]*)', str(date_divs))
    return date[0]

def get_text(bs):
    # 네이버는 에디터에 따라 css selctor가 달라진다
    text_divs1 = bs.select('.se_textView > .se_textarea > span,p')
    text_divs2 = bs.select('.post_ct span')

    if len(text_divs1) > len(text_divs2):
        final_text_div = text_divs1
    else:
        final_text_div = text_divs2

    text_for_blog = ''
    for text in final_text_div:
        text = re.sub(r'(\<.+?\>)', '', str(text))
        if text not in text_for_blog:
            text_for_blog += text
    print('text :', text_for_blog)
    return text_for_blog

def get_title(bs):
    title_divs = bs.select('.se_title > .se_textView > .se_textarea')
    if title_divs == []:
        title_divs = bs.select('.tit_h3')
    for title in title_divs:
        final_title = re.sub(r'(\s\s[\s]+)', '', str(title.text))
        return final_title

import xlwt
def save_xlsx(path, sheet_name, index_0_value, list1, list2, list3):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)
    index = 0
    for date, title, text in zip(dates, titles, texts):
        ws.write(index, 0, keyword)
        ws.write(index, 1, date)
        ws.write(index, 2, title)
        ws.write(index, 3, text)
        index += 1
    wb.save(path)

save_xlsx(XLSX_PATH, 'nanohana', '나노하나', dates, titles, texts)
