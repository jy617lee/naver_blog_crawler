from crawl import *
from settings import END_DATE, START_DATE, KEYWORD, XLSX_PATH

start = START_DATE
end = END_DATE
keyword = KEYWORD

driver = webdriver.Chrome(WEB_DRIVER_PATH)
basic_url = make_basic_url(keyword, start, end)
blog_postings = get_blog_posting_urls(basic_url, driver)

for posting_addr in blog_postings:
    posting_addr = posting_addr[0]
    blog_base_url = 'https://m.blog.naver.com/'
    url = blog_base_url + posting_addr
    get_element(url, driver)

save_xlsx(XLSX_PATH, KEYWORD, KEYWORD, dates, titles, texts)
