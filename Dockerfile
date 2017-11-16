FROM python:2.7-alpine
WORKDIR /usr/src/app
RUN pip install --no-cache-dir scrapy requests pymongo ujson APScheduler
RUN apk update \
  && apk add --virtual build-deps gcc musl-dev \
  && apk del build-deps
RUN rm -rf /var/cache/apk/*

COPY . .
CMD [ "python", "./start.py" ]