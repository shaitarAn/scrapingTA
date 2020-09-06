# -*- coding: utf-8 -*-
import scrapy
import re
import base64
from scrapy.loader import ItemLoader
from ..items import ExampleItem
from pathlib import Path
import csv

# infile = Path('/Users/anastassiashaitarova/reAdvisor/DBs/hotels_Austria_urls.txt')
# pathlist = Path('/Users/anastassiashaitarova/reAdvisor/DBs/').glob('**/hotels_*.txt')
BASE_DIR = Path('/Users/anastassiashaitarova/reAdvisor/data/urls/hotels_urls')
countries = re.compile(r'/hotels_(Ireland|New|UK|Can|Australia|USA).*\.txt')
# countries = re.compile(r'/hotels_Austria.*\.txt')
outfile = format('/Users/anastassiashaitarova/reAdvisor/data/output/bad_urls.csv')


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = []

    def __init__(self):
        super(ExampleSpider, self).__init__()
        for item in BASE_DIR.glob(r'**/*'):
            match = re.search(pattern=countries, string=str(item))
            if match:
                with open(item, 'r') as inf:
                    for url in inf.readlines():
                        self.start_urls.append(url.strip())

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u,
                                 callback=self.parse,
                                 meta=dict(main_url=u),
                                 dont_filter=True)

    def errback_page(self, failure):
        yield dict(main_url=failure.request.meta['main_url'],)
        # print('FAILURE', failure.request.meta['main_url'])

    def parse(self, response):
        current_url = response.url

        l = ItemLoader(item=ExampleItem(), response=response)

        id_patternD = re.compile(r'.+(d\d+).+')
        # id_patternG = re.compile(r'.+(g\d+).+')

        try:
            id = id_patternD.match(current_url).group(1)
        except AttributeError:
            new_url = response.meta['main_url']

            l.add_value('bad_url', response.url)
            l.add_value('new_url', new_url)
            yield l.load_item()
