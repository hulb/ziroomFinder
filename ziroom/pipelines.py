# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

class ZiroomPipeline(object):
    def __init__(self, mongoURI, mongoDB):
        self.mongoURI = mongoURI
        self.mongoDB = mongoDB

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongoURI = crawler.settings.get('MONGO_URI'),
            mongoDB = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(*self.mongoURI)
        self.tdb = self.connection[self.mongoDB]
        self.rooms = self.tdb.rooms

    def process_item(self, item, spider):
        if not item['lat'] or not item['lng']:
            raise DropItem("missing gps data")

        self.rooms.insert_one(dict(item))
        return item

    def close_spider(self, spider):
       self.connection.close() 