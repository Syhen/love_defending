# -*- coding: utf-8 -*-

import json
import time
import datetime
from urllib import urlencode

import pymongo
from scrapy import Spider, Request
from scrapy.conf import settings

from ld_crawler.items import VideoListItem


class VideoListSpider(Spider):
    name = "video_list"

    allowed_domains = ["v.qq.com"]

    @staticmethod
    def generate_date_list():
        id_list = [34965, 34961, 34980, 34996, 34986, 44887, 54192, 73047]
        start_year = 2011
        start_month = 6
        today = datetime.datetime.now()
        end_year = today.year
        end_month = today.month
        host = 'http://s.video.qq.com'
        path = '/get_playsource?'
        payload = {
            'id': 34986,
            'plat': 2,
            'type': 4,
            'data_type': 3,
            'video_type': 10,
            'year': 2011,
            'month': 6,
            'plname': 'qq',
            'otype': 'json',
            'callback': 'jsonp_12_0801',
            '_t': 0
        }
        for i, year in enumerate(range(start_year, end_year + 1)):
            payload['id'] = id_list[i]
            start_month = start_month if year == start_year else 1
            for month in range(start_month, 12 + 1):
                payload['year'] = year
                payload['month'] = month
                payload['_t'] = int(time.time())
                url = host + path + urlencode(payload)
                yield url
                if year == end_year and month == end_month:
                    break

    @staticmethod
    def str2num(num):
        if u'万' in num:
            return int(float(num[:-1]) * 10000)
        if u'千' in num:
            return int(float(num[:-1]) * 1000)
        return int(num)

    def start_requests(self):
        urls = self.generate_date_list()
        mongo_uri = settings.get("MONGO_URI")
        db_name = settings.get("DB_NAME")
        auth = settings.get("AUTH")
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name]
        if auth:
            db.authenticate(**auth)
        data = db['video_list'].find({}, {'_id': 1})
        self.video_ids = set(i['_id'] for i in data)
        for url in urls:
            yield Request(
                url,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        data = json.loads(response.body[len('jsonp_12_0801('): -1])
        for i in data['PlaylistItem']['videoPlayList']:
            item = VideoListItem()
            item['id'] = i['id']
            title = i['title'].split()
            item['title'] = title[1]
            item['date_str'] = title[0]
            item['img_url'] = i['pic']
            item['total_views'] = self.str2num(i['thirdLine'])
            item['url'] = i['playUrl']
            item['date'] = datetime.datetime.strptime(title[0], '%Y-%m-%d')
            item['views_per_day'] = int(item['total_views'] * 1. / ((datetime.datetime.now() - item['date']).days + 1))
            if item['id'] not in self.video_ids:
                yield Request(
                    item['url'],
                    meta={'item': item},
                    callback=self.parse_seconds,
                    dont_filter=True
                )
            else:
                yield item

    def parse_seconds(self, response):
        item = response.meta['item']
        item['seconds'] = int(response.xpath('//li[@class="list_item current"]/@tl').extract()[0])
        m, s = divmod(item['seconds'], 60)
        h, m = divmod(m, 60)
        item['duration'] = ("%02d:%02d:%02d" % (h, m, s))
        yield item
