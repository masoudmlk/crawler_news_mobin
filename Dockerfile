FROM python:3.8-alpine

WORKDIR /crawler_news_mobin

COPY requirements.txt /crawler_news_mobin/requirements.txt

RUN pip install -r requirements.txt


EXPOSE 8000
