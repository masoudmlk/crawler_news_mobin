import logging
import datetime
import json
import scrapy
import persian
from core.models import News
from arz_news.arz_news.items import ArzdigitalItem



class ArzdigitalSpider(scrapy.Spider):
    name = 'arzdigital'
    allowed_domains = ['arzdigital.com']

    start_urls = []
    BITCOIN_TYPE = "bitcoin"
    ETHEREUM_TYPE = "ethereum"
    ALL_TYPE = "all"
    page_number = {}
    type_news = None
    URLS_BY_TYPE = {BITCOIN_TYPE: 'https://arzdigital.com/category/news/bitcoin-news/',
                    ETHEREUM_TYPE: 'https://arzdigital.com/category/news/ethereum-news/'}

    def __init__(self, typeNews='all'):
        self._set_start_urls(typeNews)

    def _set_start_urls(self, typeNews):
        if typeNews == self.ALL_TYPE:
            self.start_urls.append(self.URLS_BY_TYPE[self.BITCOIN_TYPE])
            self.start_urls.append(self.URLS_BY_TYPE[self.ETHEREUM_TYPE])
        elif typeNews == self.BITCOIN_TYPE:
            self.start_urls.append(self.URLS_BY_TYPE[self.BITCOIN_TYPE])
        elif typeNews == self.ETHEREUM_TYPE:
            self.start_urls.append(self.URLS_BY_TYPE[self.ETHEREUM_TYPE])

    def initial_value_for_type_news(self, response):
        self.type_news = response.request.meta.get('type_news')

        if self.type_news is None:
            if response.url == self.URLS_BY_TYPE[self.BITCOIN_TYPE]:
                self.type_news = self.BITCOIN_TYPE
            elif response.url == self.URLS_BY_TYPE[self.ETHEREUM_TYPE]:
                self.type_news = self.ETHEREUM_TYPE
            else:
                # todo I dont have any idea now
                pass

    def check_exists_in_db(self, links):
        list_title = []
        for link in links:
            title = self.get_title_url(link)
            list_title.append(title)

        news = News.objects.filter(title_url__in=list_title)

        status = (len(news) == len(list_title))

        return status

    def parse(self, response, **kwargs):
        self.initial_value_for_type_news(response)
        # open_in_browser(response)
        page_links = response.xpath("//div[@class='arz-row-sb arz-posts']/a/@href").getall()
        next_page = response.xpath("//div[@class='arz-pagination']/ul/li[@class='arz-pagination__item arz-active']/following-sibling::node() [1]/a/@href").get()

        next_page_active = True
        for page_link in page_links:
            title_url = self.get_title_url(page_link)
            news_exists = News.objects.filter(title_url=title_url, type_news=self.type_news).exists()
            if not news_exists:
                next_page_active = True
                yield response.follow(url=response.urljoin(page_link), callback=self.parse_news_entity,
                                      meta={'type_news': self.type_news}, dont_filter=True)

        if next_page_active:
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'type_news': self.type_news})

    @staticmethod
    def get_title_url(link):
        ret = link.split("/")
        title = ret[-2] if len(ret) > 2 else None
        return title

    @staticmethod
    def get_type_url(link):
        ret = link.split("/")
        type = ret[-4] if len(ret) > 4 else None
        return type

    def parse_news_entity(self, response):
        year, month, day = str(response.xpath("//time/@datetime").get()).split("-")

        persian_datetime = response.xpath("//time/text()").get()
        date_persian, time_persian = str(persian_datetime).split("|")
        hour, minute = str(time_persian).strip().split(":")
        hour, minute = persian.convert_fa_numbers(hour), persian.convert_fa_numbers(minute)
        title_url = self.get_title_url(response.url)
        # imageset = response.xpath("//article/descendant::img/@data-src").get()
        #
        # images = str(imageset).split(",")
        # image_list = []
        # for image in images:
        #     image_url = str(image).split(" ")[0]
        #     image_list.append(image_url)

        item = {
            'source': self.name,
            'type_news': response.request.meta.get("type_news"),
            'title': response.xpath("//section[@class='arz-post__header']/h1/a/text()").get(),
            'article': " ".join(response.xpath("//article//descendant-or-self::node()/text()").getall()),
            'img_article_url': response.xpath("//article/descendant::img/@data-src").get(),
            'title_url': title_url,
            'url': response.url,
            'author': response.xpath("//span[@class='arz-post__info-author-name']/a/text()").get(),
            'author_link': response.xpath("//span[@class='arz-post__info-author-name']/a/@href").get(),
            'datetime': datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        }

        arzDigitItem = ArzdigitalItem(**item)
        arzDigitItem.save()

        yield item

    # def parse_item(self, response):
    #     print(response.url)
    #     # if not self.first:
    #     #     open_in_browser(response)
    #     #     self.first = True
    #
    #     yield {
    #         "title": response.xpath("//h1[@data-testid='hero-title-block__title']/text()").get(),
    #         # "year": response.xpath("//div[@data-testid='hero-title-block__original-title']/following-sibling::ul/li[position()=1]/a/text()").get(),
    #         "year": response.xpath("//ul[@data-testid='hero-title-block__metadata']/li[position()=1]/a/text()").get(),
    #         "genre": response.xpath(
    #             "//div[@data-testid='genres']/div[@class='ipc-chip-list__scroller']/a/span/text()").getall(),
    #         "duration": response.xpath(
    #             "//ul[@data-testid='hero-title-block__metadata']/li[position()=3]/text()").getall(),
    #
    #         "rating": response.xpath(
    #             "//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[position()=1]/text()").get(),
    #         "count_rate": response.xpath(
    #             "//div[@data-testid='hero-rating-bar__aggregate-rating__score']/parent::node()/div[position()=last()]/text()").get(),
    #         "movie_url": response.url,
    #
    #     }
    #     # title = response.xpath("//h1[@data-testid='hero-title-block__title/text()']").get()
    #
    #     # item = {}
    #     # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     # item['name'] = response.xpath('//div[@id="name"]').get()
    #     # item['description'] = response.xpath('//div[@id="description"]').get()
    #     # return item
