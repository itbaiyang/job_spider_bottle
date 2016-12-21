#!/usr/bin/python
from spider.get_content import get_content
# from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import logging
from spider.push_data import push_data
# client = MongoClient('127.0.0.1', 27017)
# db = client.spider
# collection = db.job51
base_url = 'http://zhannei.baidu.com/cse/search?s=4441874852613225620&entry=1&q='
url_spider = "https://data.api.zhironghao.com/update/job"


def get_data(html_text, company):
    bid = {}
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    content = bs.find(id='results')
    try:
        page = content.find_all(class_='result')
        link = page[0].find('a').get('href')
        company_content = get_content(link, 'utf-8')
        bs_company = BeautifulSoup(company_content, "html.parser")
        main = bs_company.find(class_='main')
        bid['companyName'] = main.find('div', class_='wrap-til').find('h1').get_text()
        job = bs_company.find(id='s_exampleJob')
        if job is not None:
            link_content = job.find_all(class_='exj-child')
            for item_link in link_content:
                link_job = item_link.find('a').get('href')
                bid['mark'] = link_job
                bid['from'] = '中华英才'
                detail_job = get_content(link_job, 'utf-8')
                bs_job = BeautifulSoup(detail_job, "html.parser")
                content_job = bs_job.find(class_="job-detail-l")
                job_profile = content_job.find(class_='job_profile')
                base_info = job_profile.find(class_="base_info")
                bid['position'] = base_info.find(class_='job_name').get_text()
                job_require = base_info.find(class_="job_require").find_all('span')
                bid['salary'] = job_require[0].get_text()
                bid['address'] = job_require[1].get_text()
                bid['jobNature'] = job_require[2].get_text()
                bid['education'] = job_require[3].get_text()
                bid['workYear'] = job_require[4].get_text()
                job_fit_tags = job_profile.find(class_="job_fit_tags").find_all('li')
                test_tag = []
                for item_tag in job_fit_tags:
                    if item_tag.string is not None:
                        test_tag.append(item_tag.string)
                bid['positionLabel'] = test_tag

                job_intro = content_job.find(class_='job_intro')
                job_intro_tag = job_intro.find(class_='job_intro_tag').get_text()
                tag_str = re.sub(r'\n|\r|\t|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', job_intro_tag)
                bid['positionAdvantage'] = tag_str
                job_intro_info = job_intro.find(class_='job_intro_info').get_text()
                info_str = re.sub(r'\n|\r|\t|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020', '', job_intro_info)
                bid['positionIntroduce'] = info_str
                print(bid)
                logging.info(bid)
                push_data(url_spider, bid)
        else:
            print('no job')
    except:
        print('no company')


def spider_job(company):
    url = base_url + company
    html = get_content(url, 'utf-8')
    get_data(html, company)
