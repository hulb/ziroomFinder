# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiRoom(scrapy.Item):
    link = scrapy.Field()
    floor = scrapy.Field()
    floor_total = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    _id = scrapy.Field()
    isBalcony = scrapy.Field()
    houseId = scrapy.Field()
    resblock_id = scrapy.Field()
    status = scrapy.Field()
    bedroom = scrapy.Field()
    parlor = scrapy.Field()
    face = scrapy.Field()
    will_unrent_date = scrapy.Field()
    tags = scrapy.Field()
    code = scrapy.Field()
    city_code = scrapy.Field()
    name = scrapy.Field()


class ZiRoomKeeper(scrapy.Item):
    phone = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()


class ZiRoomBlock(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    keeperId = scrapy.Field()
    greening_ratio = scrapy.Field()

class ZiRoomMate(scrapy.Item):
    _id = scrapy.Field()
    house_id = scrapy.Field()
    roommateGender = scrapy.Field()
    roommateHoroscope = scrapy.Field()
    title = scrapy.Field()

