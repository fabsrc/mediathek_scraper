# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MediathekScraperItem(scrapy.Item):
    id = scrapy.Field()
    type = scrapy.Field()
    channel = scrapy.Field()

    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    fsk = scrapy.Field()
    geo = scrapy.Field()

    show = scrapy.Field()

    date = scrapy.Field()
    duration = scrapy.Field()
    ttl = scrapy.Field()

    files = scrapy.Field()
