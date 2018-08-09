from crawl import *
from settings import END_DATE, START_DATE, KEYWORD, XLSX_PATH

start = START_DATE
end = END_DATE
keyword = KEYWORD
driver = webdriver.Chrome(WEB_DRIVER_PATH)

# 키워드, 검색 시작/종료 날짜의 포스팅을 보여주는 basic_url 만들기
basic_url = make_basic_url(keyword, start, end)

# basic_url을 통해 검색되는 블로그 포스팅 url들을 모은 blog_postings 만들기
blog_postings = get_blog_posting_urls(basic_url, driver)

# blog_postings의 date, text, title 가져오기
get_posting_elements(blog_postings)

# XLSX_PATH에 저장하기
save_xlsx(XLSX_PATH, KEYWORD, KEYWORD, dates, titles, texts)
