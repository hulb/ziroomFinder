#!-*-coding:utf-8-*

import scrapy
from scrapy.selector import HtmlXPathSelector
from ziroom.items import ZiRoom, ZiRoomKeeper, ZiRoomBlock, ZiRoomMate
from scrapy.linkextractors import LinkExtractor
import ujson


class ZiroomSpider(scrapy.Spider):
    name = 'ziroomFinder'

    def __init__(self):
        super(ZiroomSpider, self).__init__()
        self.headers = headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.API_headers = {
            'Accept': 'application/json;version=2',
            'Content-Type': 'application/json'
        }
        self.statusDict = {
            'dzz': '待入住',
            'zzz': '转租中',
            'ycz': '已入住',
            'tzpzz': '待入住',
            'yxd': '已预订'
        }

    def start_requests(self):
        urls = [
            'http://sh.ziroom.com/z/nl/z3-r1-o4.html',
            'http://sh.ziroom.com/z/nl/z3-r2-o4.html'
            ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseList, headers=self.headers)

    def parseList(self, response):
    
        # extractor other path link to crawl
        extractor = LinkExtractor(allow=(r'^http://sh\.ziroom\.com/z/nl/z3-r1-o4\.html\?p=\d', r'^http://sh\.ziroom\.com/z/nl/z3-r2-o4\.html\?p=\d'))
        for link in extractor.extract_links(response):
            yield scrapy.Request(url=link.url, headers=self.headers, callback=self.parseList)

        for house in response.css('li.clearfix'):
            room = ZiRoom()
            detail = house.css('div.detail p span::text').extract()
            room['link'] = 'http:' + house.css('h3 a::attr(href)').extract_first()
            room['_id'] = room['link'].split('/')[-1][:-5]

            yield scrapy.Request(url=room['link'], meta={'room': room, 'roomId': room['_id']}, headers=self.headers, callback=self.parseRoom)

    def parseRoom(self, response):
        roomInfo = response.meta.get('room', ZiRoom())
        roomInfo['houseId'] = response.css('input#house_id::attr(value)').extract_first()
        roomInfo['resblock_id'] = response.css('input#resblock_id::attr(value)').extract_first()
        roomInfo['city_code'] = response.css('input#curCityCode::attr(value)').extract_first()

        yield scrapy.Request(url='http://sh.ziroom.com/detail/steward?resblock_id=%s' % roomInfo['resblock_id'], meta={'keeperBlockId': roomInfo['resblock_id']}, headers=self.headers, callback=self.parseKeeper)
        yield scrapy.Request(url='http://phoenix.ziroom.com/v7/room/detail.json?house_id=%s&id=%s&city_code=%s' % (roomInfo['houseId'], roomInfo['_id'], roomInfo['city_code']), meta={'room': roomInfo, 'roomId': roomInfo['_id']}, headers=self.API_headers, callback=self.parseRoomByAPI)

    def parseRoomByAPI(self, response):
        roomResponse = ujson.loads(response.body).get('data', {})
        if roomResponse:
            roomInfo = response.meta.get('room', ZiRoom())
            roomInfo['code'] = roomResponse.get('code', '')
            status = roomResponse.get('status', '')
            roomInfo['status'] = self.statusDict.get(status, status)
            roomInfo['price'] = roomResponse.get('price', '')
            roomInfo['size'] = roomResponse.get('area', '')
            roomInfo['face'] = roomResponse.get('face', '')
            roomInfo['bedroom'] = roomResponse.get('bedroom', '')
            roomInfo['parlor'] = roomResponse.get('parlor', '')
            roomInfo['floor'] = roomResponse.get('floor', '')
            roomInfo['floor_total'] = roomResponse.get('floor_total', '')
            roomInfo['will_unrent_date'] = roomResponse.get('will_unrent_date', '')
            roomInfo['_id'] = roomResponse.get('id', '')
            roomInfo['city_code'] = roomResponse.get('city_code', '')
            roomInfo['_id'] = roomResponse.get('id', '')

            resblock = roomResponse.get('resblock', {})
            space = roomResponse.get('space', [{}])[0]
            roommates = roomResponse.get('roommates', [])

            roomInfo['tags'] = [item['title'] for item in space.get('tags', []) if 'title' in item]
            roomInfo['name'] = space.get('name', '')
            roomInfo['isBalcony'] = True if u'\u72ec\u7acb\u9633\u53f0' in roomInfo['tags'] else False

            block = ZiRoomBlock()
            block['_id'] = resblock.get('id', '')
            block['name'] = resblock.get('name', '')
            block['lat'] = resblock.get('lat', '')
            block['lng'] = resblock.get('lng', '')
            block['greening_ratio'] = resblock.get('greening_ratio', '')

            roomInfo['resblock_id'] = block['_id']

            for item in roommates:
                roommate = ZiRoomMate()
                roommate['_id'] = item.get('id', '')
                roommate['house_id'] = item.get('house_id', '')
                roommate['title'] = item.get('title', '')
                roommate['roommateGender'] = item.get('roommate_gender', '')
                roommate['roommateHoroscope'] = item.get('roommate_horoscope', '')

                mateRoomInfo = ZiRoom()
                mateRoomInfo['houseId'] = roommate['house_id']
                mateRoomInfo['_id'] = roommate['_id']

                yield scrapy.Request(url='http://phoenix.ziroom.com/v7/room/detail.json?house_id=%s&id=%s&city_code=%s' % (roommate['house_id'], roommate['_id'], roomInfo['city_code']), meta={'room': roomInfo, 'roomId': roommate['_id']}, headers=self.API_headers, callback=self.parseRoomByAPI)
                yield roommate
            
            yield roomInfo

    def parseKeeper(self, response):
        keeperResponse = ujson.loads(response.body).get('data', {})
        if keeperResponse:
            keeper = ZiRoomKeeper()
            keeper['_id'] = keeperResponse.get('keeperId', '')
            keeper['name'] = keeperResponse.get('keeperName', '')
            keeper['phone'] = keeperResponse.get('keeperPhone', '')

            yield keeper


