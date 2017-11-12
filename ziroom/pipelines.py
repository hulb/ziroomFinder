# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import DropItem
from ziroom.items import ZiRoom, ZiRoomKeeper, ZiRoomBlock, ZiRoomMate

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
        self.blocks = self.tdb.blocks
        self.keepers = self.tdb.keepers
        self.roommates = self.tdb.roommates

    def process_item(self, item, spider):
        if isinstance(item, ZiRoom):
            # use mongodb _id field to filter duplicated item
            try:
                self.rooms.insert_one(dict(item))
            except DuplicateKeyError, error:
                raise DropItem("room exists")

        if isinstance(item, ZiRoomKeeper):
            try:
                self.keepers.insert_one(dict(item))
            except DuplicateKeyError, error:
                raise DropItem("keeper exists")
        
        if isinstance(item, ZiRoomBlock):
            try:
                self.blocks.insert_one(dict(item))
            except DuplicateKeyError, error:
                raise DropItem("block exists")

        if isinstance(item, ZiRoomMate):
            try:
                self.roommates.insert_one(dict(item))
            except DuplicateKeyError, error:
                raise DropItem("roommate exists")

        return item

    def close_spider(self, spider):
       self.connection.close() 