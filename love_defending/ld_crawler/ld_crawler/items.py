# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoListItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    total_views = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    date_str = scrapy.Field()
    updated_at = scrapy.Field()
    seconds = scrapy.Field()
    duration = scrapy.Field()
