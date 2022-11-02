import json

from celery import shared_task
from time import sleep
from arz_news.arz_news.spiders.arzdigital import ArzdigitalSpider
from arz_news.arz_news.spiders.eghtesadnews import EghtesadnewsSpider
from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings
from multiprocessing import Process

@shared_task
def notify_task(message):
    print("sending 10k emails")
    print(message)
    sleep(10)
    print("Email were successfully send!")


def run_scrapy(spiderItemStr='arzdigital,eghtesadnews', typeNews='all'):
    spider_item = spiderItemStr.split(',')
    process = CrawlerProcess(get_project_settings())
    if 'arzdigital' in spider_item:
        process.crawl(ArzdigitalSpider, typeNews=typeNews)
    if 'eghtesadnews' in spider_item:
        process.crawl(EghtesadnewsSpider, typeNews=typeNews)
    process.start()


@shared_task
def crawl_news(spiderItemStr='arzdigital,eghtesadnews', typeNews='all'):
    p =Process(target=run_scrapy, args=(spiderItemStr, typeNews))
    p.start()
    p.join()


from scrapy import signals
from scrapy.crawler import Crawler
from twisted.internet import reactor







# def crawl_news(arzdigital=None, eghtesadNews=None, typeNews='all'):
#     arzdigital = json.loads(arzdigital)
#     eghtesadNews = json.loads(eghtesadNews)
#
#     process = CrawlerProcess(get_project_settings())
#
#     if arzdigital is not None:
#         process.crawl(arzdigital, typeNews=typeNews)
#     if eghtesadNews is not None:
#         process.crawl(eghtesadNews, typeNews=typeNews)
#     process.start()
