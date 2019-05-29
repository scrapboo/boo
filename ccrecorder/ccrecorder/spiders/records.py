# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CSVFeedSpider
from ccrecorder.items import CCrecord


class RecordsSpider(CSVFeedSpider):
    name = 'records'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed.csv']
    headers = ['pin']
    # NO_PINS_FOUND_RESPONSE_XPATH = '//html/body/div[4]/div/div/div[2]/div/div/p[2]/text()'
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        pin = row['pin']
        return scrapy.Request('https://www.ccrecorder.org/parcels/search/parcel/result/?line='+pin,
                              callback=self.parse_pin_page)

    def parse_pin_page(self, response):
        self.log(response.xpath('//html/body/div[4]/div/div/div[2]/div/div/p[2]/text()').extract_first())

        item = CCrecord()    #import the scrapy.item container.

        self.log('I came to this point from url '+response.url)
        # Extract the top 'card'
        #item['top_card'] = self.get()
        # Extract the table of documents

        yield item
