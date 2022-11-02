from django.contrib import admin
from django.urls import path, include
from core import views
from time import sleep
from django.http import HttpResponse
from core.tasks import notify_task



def test(request):
    notify_task.delay('hello masoud')
    return HttpResponse("ok")


urlpatterns = [
    path(r"news/", views.ScrapNews.as_view({'get': 'list'})),
    path(r"news/force_crawl/", views.ForceScrapNews.as_view()),
    path("test/", test)
]