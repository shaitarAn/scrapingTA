# -*- coding: utf-8 -*-
import scrapy
import re
import base64
from scrapy.loader import ItemLoader
from ..items import ExampleItem
from pathlib import Path

# infile = Path('/Users/anastassiashaitarova/reAdvisor/DBs/hotels_Austria_urls.txt')
# pathlist = Path('/Users/anastassiashaitarova/reAdvisor/DBs/').glob('**/hotels_*.txt')
BASE_DIR = Path('/Users/anastassiashaitarova/reAdvisor/DBs/hotels_urls')
countries = re.compile(r'/hotels_(Ireland|New|UK|Can|Australia|USA).*\.txt')
# countries = re.compile(r'/hotels_Ireland.*\.txt')


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

    def parse(self, response):
        current_url = response.url

        domain_pattern = re.compile(r'(https://\w+\.tripadvisor.+)/')
        domain = domain_pattern.match(current_url).group(1)

        id_pattern = re.compile(r'.+(d\d+).+')
        id = id_pattern.match(current_url).group(1)

        true_url = response.xpath('//div[@data-blcontact="URL_HOTEL "]/a/@data-encoded-url').get()
        url_pattern = re.compile(r'.+(/.+)$')
        if true_url:
            my_url = base64.b64decode(true_url.encode())
            full_url = domain + url_pattern.match(my_url.decode()).group(1)
        else:
            full_url = "not available"

        country = response.xpath(
            '//div[@class="_39sLqIkw" and text()="LOCATION"]/following::div[1]/text()').get()
        print(country)

        l = ItemLoader(item=ExampleItem(), response=response)
        l.add_xpath('hotelname', '//h1[@id="HEADING"]/text()')
        l.add_value('hotelurl_ontripadvisor', response.url)
        l.add_value('uniq_id', id)
        l.add_value('country', country)
        #
        yield l.load_item()
