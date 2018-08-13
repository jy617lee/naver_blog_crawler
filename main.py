from crawl import *
from settings import *
driver = webdriver.Chrome(WEB_DRIVER_PATH)
index = 0
wb = xlwt.Workbook()
ws = wb.add_sheet('naver_blog')
for start_date, end_date, dining_name, broad_date in zip(START_DATE, END_DATE, DINING_NAME, BROAD_DATE):
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    blog_posting_urls = get_blog_posting_urls(dining_name, start_date, end_date, driver)
    print(start_date, end_date, dining_name, BROAD_NAME, broad_date)
    # blog_postings의 date, text, title 가져오기
    dates = []
    titles = []
    texts = []

    for posting_addr in blog_posting_urls:
        date = get_element(DATE, posting_addr, driver)
        dates.append(date)

        text = get_element(TEXT, posting_addr, driver)
        texts.append(text)

        title = get_element(TITLE, posting_addr, driver)
        titles.append(title)

    # XLSX_PATH에 저장하기
    index = save_xlsx(wb, ws, BROAD_NAME, dining_name, broad_date, dates, titles, texts, index)
    wb.save(XLSX_PATH)
