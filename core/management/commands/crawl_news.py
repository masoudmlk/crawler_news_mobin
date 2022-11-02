from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import CrawlerProcess
from arz_news.arz_news.spiders.arzdigital import ArzdigitalSpider
from arz_news.arz_news.spiders.eghtesadnews import EghtesadnewsSpider
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = 'Edits the specified blog post.'
    LIST_SPIDERS = {'arzdigital': ArzdigitalSpider, 'eghtesadnews': EghtesadnewsSpider}
    ALL = 'all'
    def add_arguments(self, parser):
        parser.add_argument('seeder', type=str, help="name of your website or spider. choice arzdigital or eghtesadnews")

        # optional arguments
        parser.add_argument('-t', '--type', type=str, help='Indicate the type of the news.')
        # parser.add_argument('-c', '--content', type=str, help='Indicate new blog post content.')

    def handle(self, *args, **options):
        typeNews = options.get('type')
        seeder = options['seeder']
        typeNews = self.ALL if typeNews is None else typeNews
        spiderList = [self.LIST_SPIDERS.values() if self.LIST_SPIDERS.get(seeder) is None else self.LIST_SPIDERS.get(seeder)]

        process = CrawlerProcess(get_project_settings())
        for spider in spiderList:
            process.crawl(spider, typeNews=typeNews)

        self.stdout.write(self.style.SUCCESS('spider: start crawling'))
        process.start()
        self.stdout.write(self.style.SUCCESS('spider: end crawling'))

        self.stdout.write(self.style.SUCCESS(f'{typeNews} {spiderList} {seeder}'))

