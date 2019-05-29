# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CSVFeedSpider
from ccrecorder.items import CCrecord


class RecordsSpider(CSVFeedSpider):
    name = 'records'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed.csv']
    headers = ['pin']
    BASE_URL = 'http://www.ccrecorder.org'
    #
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        pin = row['pin']
        return scrapy.Request('https://www.ccrecorder.org/parcels/search/parcel/result/?line='+pin,
                              callback=self.parse_pin_page)

    def parse_pin_page(self, response):
        NO_PINS_FOUND_RESPONSE_XPATH = '//html/body/div[4]/div/div/div[2]/div/div/p[2]/text()' # where it can be
        NOT_FOUND = response.xpath(NO_PINS_FOUND_RESPONSE_XPATH).get()  # what is there
        if NOT_FOUND:                                                   # ?  (can't do without this, because of None)
            if NOT_FOUND.startswith('No PINs'):                         # No PINs?
                self.log('Not found PIN '+response.url)                 # Debug notification
                yield None                                              # and get out of here.

            else:
                self.log('something is in the place of Not found but it is not it')
                yield None

        else:                                                           # there is a PIN like that
            item = CCrecord()                                           # import the scrapy.item container.
            record_number = response.xpath('//*[@id="objs_body"]/tr/td[4]/a/@href').get().re('[.0-9]+')
            self.log('record number:  '+record_number)     # the movable debug line.
            # Extract the top 'card'
            #item['top_card'] = self.get()
            # Extract the table of documents
            yield item

'''
scrapy shell -s USER_AGENT="Mozilla/5.0" 
.re('[.0-9]+')
'''