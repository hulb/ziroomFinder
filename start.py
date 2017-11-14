# -*- coding: utf-8 -*-

import multiprocessing
import scrapy
from scrapy.crawler import CrawlerProcess
from ziroom.spiders.ziroomSpider import ZiroomSpider
import pymongo
from ziroom.settings import MONGO_DB, MONGO_URI

def crawlWorker():
    process = CrawlerProcess()
    process.crawl(ZiroomSpider)
    process.start()

if __name__ == '__main__':
    # start 2 process, one for update room status , one for crawl new rooms
    p = multiprocessing.Process(target=crawlWorker)
    p.start()


