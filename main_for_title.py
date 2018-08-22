from crawl_title_only import *
from settings import *
from selenium import webdriver
import xlwt

driver = webdriver.Chrome(WEB_DRIVER_PATH)
wb = xlwt.Workbook()
ws = wb.add_sheet('blogs')
index = 0

for start_date, end_date, dining_name, broad_date \
in zip(START_DATE, END_DATE, DINING_NAME, BROAD_DATE):
    blog_postings = get_date_and_title(dining_name, start_date, end_date, driver)
    index = save_xlsx(wb, ws, index, BROAD_NAME, dining_name, broad_date,
                        blog_postings.get('dates'),
                        blog_postings.get('titles'),
                        blog_postings.get('addrs'))


wb.save(XLSX_PATH)
