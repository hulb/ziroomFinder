FROM python:2.7-alpine
WORKDIR /usr/src/app
RUN pip install --no-cache-dir scrapy requests pymongo ujson APScheduler
RUN rm -rf /var/cache/apk/*

COPY . .
CMD [ "python", "./start.py" ]