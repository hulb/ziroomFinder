# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

statusDict = {
    'dzz': '待入住',
    'zzz': '转租中',
    'ycz': '已入住',
    'tzpzz': '待入住',
}

class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    floor = scrapy.Field()
    allfloor = scrapy.Field()
    town = scrapy.Field()
    layout = scrapy.Field()
    nearbymetroline = scrapy.Field()
    nearbymetrostation = scrapy.Field()
    nearbymetrodistance = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    size = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    _id = scrapy.Field()
    isBalcony = scrapy.Field()
    houseId = scrapy.Field()
    resblock_id = scrapy.Field()


class ZiroomKeeper(scrapy.Item):
    phone = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()


