from crawl import *
from settings import END_DATE, START_DATE, KEYWORD, XLSX_PATH

start = START_DATE
end = END_DATE
keyword = KEYWORD

driver = webdriver.Chrome(WEB_DRIVER_PATH)
basic_url = make_basic_url(keyword, start, end)
blog_postings = get_blog_posting_urls(basic_url, driver)
get_posting_elements(blog_postings)


save_xlsx(XLSX_PATH, KEYWORD, KEYWORD, dates, titles, texts)
