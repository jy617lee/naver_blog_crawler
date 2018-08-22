from urllib import request, parse
from bs4 import BeautifulSoup
import re

def make_search_url(keyword, start, end):
    print('make_basic_url')
    base_url = 'https://m.search.naver.com/search.naver?display=15&nso=p%3A'
    period = 'from' + start + 'to' + end
    query = '&query=' + parse.quote(keyword)
    end = '&where=m_blog&start='
    final_url = base_url + period + query + end
    return final_url

TITLE = 0
DATE = 1
ADDR = 2

def get_date_and_title(keyword, start, end, driver):
    blog_dates = []
    blog_titles = []
    blog_addrs = []
    blog_postings = {
        'dates' : blog_dates,
        'titles' : blog_titles,
        'addrs' : blog_addrs,
    }
    index = 1;
    flag = True

    url = make_search_url(keyword, start, end)

    while(flag):
        url_final = url + str(index)
        driver.get(url_final)
        html = driver.page_source
        bs = BeautifulSoup(html, 'html5lib')
        blogs = bs.select('.lst_total > .bx')
        for blog in blogs:
            blog_date = get_element(DATE, blog)
            blog_title = get_element(TITLE, blog)
            blog_addr = get_href(blog)

            if blog_addr in blog_addrs:
                flag = False
                break
            else:
                blog_dates.append(blog_date)
                blog_titles.append(blog_title)
                blog_addrs.append(blog_addr)
        index += 15
    return blog_postings

def get_element(type, bs):
    switcher = {
        TITLE : '.total_tit',
        DATE : '.sub_time',
    }

    res = bs.select(switcher.get(type))
    res = re.findall(r'>(.+)<\/', str(res))[0]
    return res

def get_href(bs):
    res = bs.select('a')
    res = re.findall(r'href=\"(.+)\sonclick', str(res))[0]
    return res

def save_xlsx(wb, ws, index, broad_name, dining_name, \
            broad_date, posting_dates, posting_titles, posting_addrs):
    print('save_xlsx')

    for date, title, addr in zip(posting_dates, posting_titles, posting_addrs):
        ws.write(index, 0, broad_name)
        ws.write(index, 1, dining_name)
        ws.write(index, 2, broad_date)
        ws.write(index, 3, date)
        ws.write(index, 4, title)
        ws.write(index, 5, addr)
        index += 1

    return index

class Blog:
    def __init__(self):
        self._date = ''
        self._title = ''
        self._addr = ''

    def set_posting_info(self, date, title, addr):
        self._date = date
        self._title = title
        self._addr = addr

    def get_title(self):
        return self._title

    def get_date(self):
        return self._date

    def get_addr(self):
        return self._addr
