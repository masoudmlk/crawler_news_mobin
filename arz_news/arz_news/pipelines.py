# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from arz_news.items import ArzdigitalItem
from asgiref.sync import sync_to_async
import logging
from core.models import News
class ArzNewsPipeline:

    def process_item(self, item, spider):

        # news = News.objects.filter(type_news=item['type_news'],
        #                     source=item['source'],
        #                     title_url=item['title_url']).first()
        # if news is None:
        #     arzDigitItem = ArzdigitalItem(**item)
        #     # sync_to_async(arzDigitItem.save)()
        #     arzDigitItem.save()
        with open("masoud.text", "a+") as ap:
            ap.write("fewfewfewfewfwe")


        logging.error("$"*1000)
        logging.error(f"{item}")
        arzDigitItem = ArzdigitalItem(**item)
        arzDigitItem.save()
        return item
