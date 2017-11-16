# -*- coding: utf-8 -*-

import multiprocessing
import scrapy
from scrapy.crawler import CrawlerProcess
from ziroom.spiders.ziroomSpider import ZiroomSpider
import pymongo
from ziroom.settings import MONGO_DB, MONGO_URI
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

def crawlWorker():
    process = CrawlerProcess()
    process.crawl(ZiroomSpider)
    process.start()

def updateWorker():
    import pdb; pdb.set_trace()
    statusDict = {
        'dzz': '待入住',
        'zzz': '转租中',
        'ycz': '已入住',
        'tzpzz': '待入住',
        'yxd': '已预订'
    }

    roomAPI = 'http://phoenix.ziroom.com/v7/room/detail.json?house_id=%s&id=%s&city_code=%s'
    headers = {
        'Accept': 'application/json;version=2',
        'Content-Type': 'application/json'
    }
    connection = pymongo.MongoClient(*MONGO_URI)
    tdb = connection[MONGO_DB]
    rooms = tdb.rooms
    for room in rooms.find():
        roomId = room['_id']
        houseId = room['houseId']
        city_code = room['city_code']

        response = requests.get(roomAPI % (houseId, roomId, city_code), headers=headers)
        roomInfo = response.json().get('data', {})
        status = roomInfo.get('status', '')
        room['status'] = statusDict.get(status, status)

        rooms.save(room)



def job1():
    # start 2 process, one for update room status , one for crawl new rooms
    p = multiprocessing.Process(target=crawlWorker)
    p.start()

def job2():
    p2 = multiprocessing.Process(target=updateWorker)
    p2.start()

if __name__ == '__main__':
    schedule = BlockingScheduler()
    schedule.add_job(job1, 'interval', days=1, start_date='2017-11-11 3:22:16')
    schedule.add_job(job2, 'interval', days=1, start_date='2017-11-11 4:00:11')
    schedule.start()

    


