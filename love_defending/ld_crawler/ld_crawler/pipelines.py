# -*- coding: utf-8 -*-

import datetime
import pymongo
from scrapy.conf import settings


class LdCrawlerPipeline(object):
    def open_spider(self, spider):
        client = pymongo.MongoClient(host=settings.get("MONGO_URI"))
        db = client[settings.get("DB_NAME")]
        auth = settings.get("AUTH")
        if auth:
            db.authenticate(**auth)
        self.db = db

    def process_item(self, item, spider):
        item['updated_at'] = datetime.datetime.now()
        self.db['video_list'].update_one(
            {'_id': item['id']},
            {'$set': item},
            upsert=True
        )
        return item
