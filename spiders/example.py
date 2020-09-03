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

        pattern = re.compile(r'(https://\w+\.tripadvisor.+)/')
        domain = pattern.match(response.url).group(1)

        true_url = response.xpath('//div[@data-blcontact="URL_HOTEL "]/a/@data-encoded-url').get()
        pattern = re.compile(r'.+(/.+)$')
        if true_url:
            my_url = base64.b64decode(true_url.encode())
            full_url = domain + pattern.match(my_url.decode()).group(1)
        else:
            full_url = "not available"

        amenities = response.xpath('//div[@class="_2rdvbNSg"]/text()').getall()
        if response.xpath('//div[@class="_39sLqIkw" and text()="LOCATION"]'):
            locations = response.xpath(
                '//div[@class="_39sLqIkw" and text()="LOCATION"]/following::div[1]/text()').getall()
        elif response.xpath('//div[@class="_39sLqIkw" and text()="STANDORT"]'):
            locations = response.xpath(
                '//div[@class="_39sLqIkw" and text()="STANDORT"]/following::div[1]/text()').getall()
        other_names = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "_945zjkWf", " " ))]/text()').getall()
        if response.xpath('//div[@class="cPQsENeY"]/text()'):
            description = ' '.join(response.xpath('//div[@class="cPQsENeY"]/text()').getall())
        else:
            description = ' '.join(response.xpath('//div[@class="cPQsENeY"]/div/p/text()').getall())

        l = ItemLoader(item=ExampleItem(), response=response)
        l.add_xpath('hotelname', '//h1[@id="HEADING"]/text()')
        l.add_value('amenities', amenities)
        l.add_value('locations', locations)
        l.add_value('description', description)
        l.add_value('other_names', other_names)
        l.add_value('hotelurl_ontripadvisor', response.url)
        l.add_value('hotelurl', full_url)

        yield l.load_item()
