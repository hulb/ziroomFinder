# -*- coding: utf-8 -*-

import multiprocessing
import scrapy
from scrapy.crawler import CrawlerProcess
from ziroom.spiders.ziroomSpider import ZiroomSpider
import pymongo
from ziroom.settings import MONGO_DB, MONGO_URI
from apscheduler.schedulers.blocking import BlockingScheduler

def crawlWorker():
    process = CrawlerProcess()
    process.crawl(ZiroomSpider)
    process.start()

def job():
    # start 2 process, one for update room status , one for crawl new rooms
    p = multiprocessing.Process(target=crawlWorker)
    p.start()

if __name__ == '__main__':
    schedule = BlockingScheduler()
    schedule.add_job(job, 'interval', days=1, start_date='2017-11-11 4:22:16')
    schedule.start()

    


