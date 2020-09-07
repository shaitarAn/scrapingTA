# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    hotelname = scrapy.Field()
    hotelurl_ontripadvisor = scrapy.Field()
    hotelurl = scrapy.Field()
    amenities = scrapy.Field()
    locations = scrapy.Field()
    description = scrapy.Field()
    other_names = scrapy.Field()
    # #####
    hotelidp = scrapy.Field()
    # country = scrapy.Field()
    # new_url = scrapy.Field()
    # bad_url = scrapy.Field()
