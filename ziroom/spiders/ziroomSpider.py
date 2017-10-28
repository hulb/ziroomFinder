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
            detail = house.css('div.detail p span').extract()
            floor = detail[1].css('text').extract_first()

            room['allfloor'] = floor.split('/')[1][0:3]
            room['floor'] = floor.split('/')[0]
            room['layout'] = detail[2].css('text').extract_first()
            room['size'] = detail[0].css('text').extract_first()
            room['title'] = house.css('h3 a::text').extract_first()
            room['link'] = house.css('h3 a::attr(href)').extract_first()
            room['town'] = town[1:-1]
            room['nearbymetroline'] = metro.split(u'\u53f7\u7ebf')[0] if metro else ''
            room['nearbymetrostation'] = metro.split(u'\u53f7\u7ebf')[1] if metro else ''
