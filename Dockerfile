FROM python:2.7-alpine
WORKDIR /usr/src/app
RUN apk add --no-cache python-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev libffi-dev libxml2 libxslt
RUN pip install --no-cache-dir scrapy requests pymongo ujson APScheduler
RUN apk del python-dev gcc musl-dev openssl-dev libxml2-dev libxslt-dev
RUN apk add -U tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apk del tzdata && echo "Asia/Shanghai" > /etc/timezone
RUN rm -rf /var/cache/apk/*

COPY . .
CMD [ "python", "./start.py" ]