from urllib import parse
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
import time
import re

# url 만들고
base_url = 'https://m.search.naver.com/search.naver?display=15&nso=p%3A'
start = '20170305'
end = '20170405'
keyword = '나노하나'
def make_url(keyword, start, end):
    period = 'from' + start + 'to' + end
    query = '&query=' + parse.quote(keyword)
    end = '&where=m_blog&start='
    final_url = base_url + period + query + end
    return final_url

basic_url = make_url(keyword, start, end)

# page가 없을때까지 돌면서
index = 1
driver = webdriver.Chrome('C:\chromedriver.exe')
regex_href = r'.*https:\/\/m\.blog\.naver\.com\/(\w*\/\d*)'
blog_postings = []
flag = True
while(index < 15):
    url = basic_url + str(index)
    # index에 해당하는 html을 받아와
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
                # print(href)
    index += 15

# link를 돌면서 제목, 본문, 날짜 넣기
blog_base_url = 'https://m.blog.naver.com/'
titles = []
texts = []
dates = []

regex_text = r'>((\w*\s?.?)*)<'
for posting_addr in blog_postings:
    posting_addr = str(posting_addr).strip('[]')
    posting_addr = posting_addr.strip('\'\'')
    url = blog_base_url + posting_addr

    driver.get(url)
    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
    title_divs = bs.select('.se_title > .se_textView > .se_textarea')
    text_divs1 = bs.select('.se_textView > .se_textarea > span,p')
    text_divs2 = bs.select('.post_ct span')
    date_divs = bs.select('.se_date')
    date = re.findall(r'(20[\d\s\.\:]*)', str(date_divs))
    dates.append(date[0])

    if title_divs == []:
        title_divs = bs.select('.tit_h3')
        # print('url :', url)
        # print('text : ', text_divs)

    if len(text_divs1) > len(text_divs2):
        final_text_div = text_divs1
    else:
        final_text_div = text_divs2

    for title in title_divs:
        final_title = re.sub(r'(\s\s[\s]+)', '', str(title.text))
        print(final_title)
        titles.append(final_title)
        # print(title)

    text_for_blog = ''
    for text in final_text_div:
        text = re.sub(r'(\<.+?\>)', '', str(text))
        # text_final = re.sub(r'(<.*>)', '', text)
        # text_final = re.sub(r'([\[\]\'])', '', text_final)
        # text_final = text_final.strip('()')
        if text not in text_for_blog:
            text_for_blog += text
    texts.append(text_for_blog)

print(len(titles))
print(len(texts))
print(len(dates))

import xlwt
wb = xlwt.Workbook()
ws = wb.add_sheet('nanohana')
# ws_text = wb.add_sheet('nanohana_text')
index = 0
for date, title, text in zip(dates, titles, texts):
    ws.write(index, 0, keyword)
    ws.write(index, 1, date)
    ws.write(index, 2, title)
    ws.write(index, 3, text)
    index += 1

# index = 0
# for text in texts :
#     ws_text.write(index, 0, text)
#     index += 1
wb.save('C:/dateGirls/m3/nanohana_naver.xls')
