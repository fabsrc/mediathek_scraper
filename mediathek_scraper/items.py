# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MediathekScraperItem(scrapy.Item):
    title = scrapy.Field()
    show = scrapy.Field()
    date = scrapy.Field()
    desc = scrapy.Field()
    type = scrapy.Field()
    duration = scrapy.Field()
    files = scrapy.Field()
