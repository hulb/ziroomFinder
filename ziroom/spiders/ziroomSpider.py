#!-*-coding:utf-8-*

import scrapy
from scrapy.selector import HtmlXPathSelector
from ..items import ZiroomItem

class ZiroomSpider(scrapy.Spider):
    name = 'ziroomFinder'


    def start_requests(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        urls = ['http://sh.ziroom.com/z/nl/z3-r1-x2-o4.html?']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
    
        for house in response.css('li.clearfix'):
            room = ZiroomItem()
            town, metro = house.css('h4 a::text').extract_first().split(' ')
            detail = house.css('div.detail p span::text').extract()
            floor = detail[1][:-1]
            room['price'] = float(house.css('p.price::text').extract_first()[63:70].strip())
            room['floor'], room['allfloor'] = floor.split('/') if '/' in floor else ('', '')
            room['layout'] = detail[2]
            room['size'] = detail[0]
            room['title'] = house.css('h3 a::text').extract_first()
            room['link'] = house.css('h3 a::attr(href)').extract_first()
            room['town'] = town[1:-1]
            room['nearbymetroline'], room['nearbymetrostation'] = metro.split(u'\u53f7\u7ebf') if metro else ('', '')
            room['nearbymetrodistance'] = detail[-1].split(u'\u7ad9')[1] if u'\u7ad9' in detail[-1] else ''
            for key, value in room.iteritems():
                print value,
            
            print '\n'

