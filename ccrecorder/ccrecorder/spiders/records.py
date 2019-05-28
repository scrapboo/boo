# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CSVFeedSpider
from ccrecorder.items import CCrecord


class RecordsSpider(CSVFeedSpider):
    name = 'records'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed.csv']
    headers = ['pin']
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        pin = row['pin']
        return scrapy.Request('https://www.ccrecorder.org/parcels/search/parcel/result/?line='+pin,
                              callback=self.parse_pin_page)

    def parse_pin_page(self, response):
        NO_PIN_FOUND_RESPONSE_XPATH = '//html/body/div[4]/div/div/div[2]/div/div/p[2]/text()'
        if response.xpath(NO_PIN_FOUND_RESPONSE_XPATH).get().startswith('No PINs Found'):
            yield None

        item = CCrecord()
        # Extract the top 'card'
        item['top_card'] = self.extract()
        # Extract the table of documents

        yield item
