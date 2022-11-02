from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db.models.aggregates import Avg
from django.db.models import F
from arz_news.arz_news.spiders.arzdigital import ArzdigitalSpider
from arz_news.arz_news.spiders.eghtesadnews import EghtesadnewsSpider
from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings


from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from core.models import News
from core.serializer import NewsSerializer, ForceRefreshNewsSerializer
from core.tasks import crawl_news
import json
# Create your views here.


class ScrapNews(GenericViewSet, ListModelMixin):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ForceScrapNews(APIView):
    LIST_SPIDERS = {'arzdigital': 'arzdigital', 'eghtesadnews': 'eghtesadnews'}
    ALL = 'all'

    def post(self, request):
        serializer = ForceRefreshNewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        type_news = serializer.validated_data.get('type_news')
        spider = serializer.validated_data.get('spider')

        typeNews = self.ALL if type_news is None else type_news
        spiderList = []
        if self.LIST_SPIDERS.get(spider) is not None:
            spiderList.append(self.LIST_SPIDERS.get(spider))
        else:
            spiderList = list(self.LIST_SPIDERS.values())
        spiderList_str = ",".join(spiderList)
        crawl_news.delay(spiderList_str, typeNews)
        return Response(status=status.HTTP_200_OK)




    # def post(self, request):
    #     global eghteadnews
    #     serializer = ForceRefreshNewsSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     type_news = serializer.validated_data.get('type_news')
    #     spider = serializer.validated_data.get('spider')
    #
    #     typeNews = self.ALL if type_news is None else type_news
    #     arzdigtal = eghteadnews = None
    #
    #     if spider == 'arzdigital':
    #         arzdigtal = ArzdigitalSpider
    #     if spider == 'eghtesadnews':
    #         eghteadnews = EghtesadnewsSpider
    #
    #     if arzdigtal is None and eghteadnews is None:
    #         arzdigtal = ArzdigitalSpider
    #         eghteadnews = EghtesadnewsSpider
    #
    #     crawl_news.delay()
    #     return Response(status=status.HTTP_200_OK)


