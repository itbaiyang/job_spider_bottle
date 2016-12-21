#!/usr/bin/python
from spider.get_content import get_content
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import logging
from spider.push_data import push_data
client = MongoClient('127.0.0.1', 27017)
db = client.spider
collection = db.job51
base_url = 'http://search.51job.com/jobsearch/search_result.php?romJs=1&jobarea=010000%2C00&keyword='
url_spider = "https://data.api.zhironghao.com/update/job"


def get_data(html_text, company):
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    print(company)
    content = bs.find(id='resultList')
    page = content.find_all(class_='dw_tlc')
    page1 = page[0].find_all(class_='rt')
    page2 = int(re.sub(r'[^0-9]', '', page1[0].get_text())) / 50
    page3 = int(page2)+1
    for page_i in range(1, page3):
        page_str = str(page_i)
        url_page = base_url + company + '&keywordtype=1&curr_page=' + page_str
        print(url_page)
        html_page = get_content(url_page, 'gbk')
        bs = BeautifulSoup(html_page, "html.parser")  # 创建BeautifulSoup对象
        content = bs.find(id='resultList')
        li = content.find_all("div", class_='el')
        if len(li) < 1:
            print('none')
        else:
            # for i in range(1, 3):
            for i in range(1, len(li)):
                bid = {}
                position = li[i].find(class_='t1')
                company_belong = li[i].find(class_='t2')
                bid['city'] = li[i].find(class_='t3').string
                bid['salary'] = li[i].find(class_='t4').string
                bid['createDate'] = li[i].find(class_='t5').string
                bid['mark'] = position.find('a').get('href')
                bid['position'] = position.find('a').get('title')
                print(bid['position'])
                # bid['company_link'] = company_belong.find('a').get('href')
                bid['companyName'] = company_belong.find('a').get('title')

                html_detail = get_content(bid['mark'], 'gbk')
                bs_detail = BeautifulSoup(html_detail, "html.parser")
                detail_title = bs_detail.find(class_="ltype").get_text()
                clean_str = re.sub(r'\n|\r|\t|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', detail_title)
                bid['industryField'] = clean_str
                detail_content = bs_detail.find(class_="tCompany_main")
                detail_some = detail_content.find(class_="jtag")
                detail_xue = detail_some.find(class_="t1").find_all("span")
                for item in detail_xue:
                    if item.find('em', class_="i1") is not None:
                        bid['workYear'] = item.get_text()
                    elif item.find('em', class_="i2") is not None:
                        bid['education'] = item.get_text()
                    elif item.find('em', class_="i3") is not None:
                        bid['hiringNumbers'] = item.get_text()
                    # elif item.find('em', class_="i4") is not None:
                        # bid['position_date'] = item.get_text()
                if detail_some.find(class_="t2") is None:
                    print('none tag')
                else:
                    detail_tag = detail_some.find(class_="t2").find_all('span')
                    string_tag = []
                    for item_tag in detail_tag:
                        string_tag.append(item_tag.string)
                    # print(string_tag)
                    bid["positionLabel"] = string_tag
                job_msg = detail_content.find(class_="job_msg").get_text()
                clean_job = re.sub(r'\n|\r|\t|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', job_msg)
                bid['positionIntroduce'] = clean_job
                bid['from'] = '51job'
                logging.info(bid)
                # print(bid)
                push_data(url_spider, bid)
                # collection.insert(bid)


def spider_job(company):
    url = base_url + company + '&keywordtype=1&curr_page=1'
    html = get_content(url, 'gbk')
    get_data(html, company)
