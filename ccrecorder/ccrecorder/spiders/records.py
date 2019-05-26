# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from ccrrecorder.items import CCrecord


class RecordsSpider(CSVFeedSpider):
    name = 'records'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed.csv']
    prefix_url = 'https://www.ccrecorder.org/parcels/search/parcel/result/?line='
    headers = ['pin']
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        pin = row['pin']
        return scrapy.Request(prefix_url+pin, callback=self.parse_pin_page)

    def parse_pin_page(self, response):
        if response.xpath('//.../text()').extract() == ...
            yield None

        item = CC
