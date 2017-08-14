# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    start_url = scrapy.Field()
    city = scrapy.Field()
    title = scrapy.Field()
    title_url = scrapy.Field()
    new_old = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
