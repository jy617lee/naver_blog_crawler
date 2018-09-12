import xlwt
from bs4 import BeautifulSoup
from urllib import request, parse
from selenium import webdriver
from settings import WEB_DRIVER_PATH
import re

# 변수들
# district_names = ['익선동 핫', '연남동 핫', '성수동 핫', '서촌 핫', '삼청동 핫', '압구정로데오 핫', '후암동 핫', '상도동 핫', '상계동 핫', '불광동 핫', '개봉동 핫']
district_names = ['연남동 핫', '익선동 핫', '성수동 핫', '샤로수길 핫', '망원동 핫', '신사동 핫', '삼청동 핫', '명동 핫', '상도동 핫', '목동 핫', '신정동 핫', '상계동 핫']

years = []
FIRST_DAY = '0101'
LAST_DAY = '1231'
START_YEAR = 2007
END_YEAR = 2018

# 기본 셋팅
def make_years(start_year, end_year, years):
    for year in range(start_year, end_year+1):
        years.append(str(year))

make_years(START_YEAR, END_YEAR, years)
driver = webdriver.Chrome(WEB_DRIVER_PATH)
wb = xlwt.Workbook()
ws = wb.add_sheet('blogs')

base_url = "search.naver.com/search.naver?where=post&query={0}&st=sim&sm=tab_opt&date_from={1}&date_to={2}&date_to=20151231&date_option=8&srchby=all&dup_remove=1"
def crawl(district_names, years):
    row = 0;
    for district in district_names:
        print(district)
        posting_nums = []
        for index, year in enumerate(years):
            # make url
            start_day = year + FIRST_DAY
            end_day = year + LAST_DAY
            url = 'https://' + base_url.format(district, start_day, end_day)

            # 갯수 크롤링해서
            num = get_posting_num(url)
            posting_nums.append(num)

        # 엑셀에 넣기
        row = save_xlsx(district, posting_nums, ws, row)
    wb.save('C:/workspace/data_analysis/real_estimate_rent/num_of_postings_golmok.xls')

def save_xlsx(district_name, num_of_postings, ws, row):
    print('save_xlsx')
    ws.write(row, 0, district_name)
    for index, num in enumerate(num_of_postings):
        ws.write(row, index+1, num)
    return row + 1

def get_posting_num(url):
    # 건수에 해당하는 스트링 가져오기
    driver.get(url)
    html = driver.page_source
    bs = BeautifulSoup(html, 'html5lib')
    posting_nums = bs.select('.title_num')

    # 건수만 가져오기
    # print(posting_nums)
    if len(posting_nums) == 0:
        num = 0
    else:
        num = re.findall(r'([\d|\,]+)건', str(posting_nums))[0]
        num = num.replace(',', '')

    return num

crawl(district_names, years)
