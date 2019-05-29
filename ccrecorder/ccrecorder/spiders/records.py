# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CSVFeedSpider
from ccrecorder.items import CCrecord


class RecordsSpider(CSVFeedSpider):
    name = 'records'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed.csv']
    headers = ['pin']

    #
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):                                 # parse a row in CSV
        PIN_REQUEST_URL = 'https://www.ccrecorder.org/parcels/search/parcel/result/?line='
        pin = row['pin']                                                # the name of the column defined in 'headers'
        return scrapy.Request(url=PIN_REQUEST_URL + pin, callback=self.parse_pin_page)

    def parse_pin_page(self, response):
        DOCUMENTS_PAGE_URL = 'https://www.ccrecorder.org/parcels/show/parcel/'
        RECORD_NUMBER_XPATH = '//*[@id="objs_body"]/tr/td[4]/a/@href'
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
            record = CCrecord()                                         # import the scrapy.Item container.
            record_number = response.xpath(RECORD_NUMBER_XPATH).re('[.0-9]+')[0]
            record['record_number'] = record_number
            # self.log(record)     # the movable debug line.
            yield scrapy.Request(url=DOCUMENTS_PAGE_URL + record_number + '/', callback=self.parse_docs_page)

    def parse_docs_page(self, response):
        docs_dict = {'point': 'reached'}
        self.log('Reached this point')
        yield docs_dict

'''
scrapy shell -s USER_AGENT="Mozilla/5.0" 
.re('[.0-9]+')
'''