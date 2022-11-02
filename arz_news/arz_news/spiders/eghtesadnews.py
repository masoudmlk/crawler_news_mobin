from datetime import datetime
import scrapy
from core.models import News
import logging
from arz_news.arz_news.items import ArzdigitalItem


class EghtesadnewsSpider(scrapy.Spider):

    name = 'eghtesadnews'
    allowed_domains = ['eghtesadnews.com']
    start_urls = ['http://eghtesadnews.com/']

    BITCOIN_TYPE = "bitcoin"
    ETHEREUM_TYPE = "ethereum"
    ALL_TYPE = "all"
    page_number = {}
    type_news = None
    URLS_BY_TYPE = {BITCOIN_TYPE: "https://www.eghtesadnews.com/newsstudios/archive/?query=%D8%A8%DB%8C%D8%AA+%DA%A9%D9%88%DB%8C%D9%86",
                    ETHEREUM_TYPE: 'https://www.eghtesadnews.com/newsstudios/archive/?query=%D8%A7%D8%AA%D8%B1%DB%8C%D9%88%D9%85'}

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

    def check_exists_in_db(self, links_datetime):
        for link_datetime in links_datetime:
            news = News.objects.filter(title_url=str(link_datetime).strip(), source=self.name, type_news=self.type_news).first()
            if news is None:
                return False
        return True

    def parse(self, response, **kwargs):
        self.initial_value_for_type_news(response)
        # open_in_browser(response)

        page_links = response.xpath("//ul[@id='archive-page-news']/li[@class='cont']/a[@class='res']/@href").getall()
        next_page = response.urljoin(response.xpath("//footer[@class='archive-next-page']/a[position()=last()]/@href").get())

        list_datetime = response.xpath("//div[@class='news_time']//time/@datetime").getall()

        next_page_active = False
        for index_link, page_link in enumerate(page_links):
            news_exists = News.objects.filter(title_url=list_datetime[index_link], type_news=self.type_news).exists()
            if not news_exists:
                next_page_active = True
                yield response.follow(url=response.urljoin(page_link), callback=self.parse_news_entity,
                                      meta={'type_news': self.type_news}, dont_filter=True)

        if next_page_active:
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'type_news': self.type_news})

    def parse_news_entity(self, response):

        datetime_str = response.xpath("//div[@class='wrapper']/time[@class='news_time']/@datetime").get()
        datetime_str_modified = str(datetime_str).replace("Z", "").strip()
        news_datetime = datetime.fromisoformat(datetime_str_modified)

        item = {
            'source': self.name,
            'type_news': response.request.meta.get("type_news"),
            'title': str(response.xpath("//header/div[@class='title']/h1/text()").get()).strip(),
            'article': str(" ".join(response.xpath("//div[@class='body']/div[@class='innerbody']/*[not(@id='related-news')]//text()").getall())).strip(),
            'img_article_url': response.xpath("//div[@id='news-page-content']//div[@class='image']/img/@src").get(),
            'title_url': str(datetime_str).strip(),
            'url': response.url,
            'author': None,
            'author_link': None,
            'datetime': news_datetime
        }
        news = News.objects.filter(type_news=item['type_news'], source=item['source'],
                                   title_url=item['title_url']).first()
        if news is None:
            arzDigitItem = ArzdigitalItem(**item)
            arzDigitItem.save()

        yield item
