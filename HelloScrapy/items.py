# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HelloscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    region = scrapy.Field()
    nature = scrapy.Field()
    size = scrapy.Field()
    web_site = scrapy.Field()
    address = scrapy.Field()
    introduction = scrapy.Field()
