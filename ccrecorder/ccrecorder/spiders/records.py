# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CSVFeedSpider
from ccrecorder.items import CCrecord


class RecordsSpider(CSVFeedSpider):
    """
    Reads the pin feed csv file and parses the CC recorder
    for these pins.
    The pins can be 10 or 14 digit long
    """
    name = 'records'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed.csv']
    headers = ['pin']

    def parse_row(self, response, row):
        """
        Reads a row in csv and makes a request to the pin page
        :param response: the downloaded pin page
        :param row: a single PIN read from the pin feed file
        :return: yiels a scrapy.Item
        """
        PIN_REQUEST_URL = 'https://www.ccrecorder.org/parcels/search/parcel/result/?line='
        pin = row['pin']                                                # the name of the column defined in 'headers'
        return scrapy.Request(url=PIN_REQUEST_URL + pin, callback=self.parse_pin_page, meta={'pin':pin})

    def parse_pin_page(self, response):
        """
        Parses the pin page, detects if there is none, detects if
        there are multiple pins and their corresponding links on a page,
        jumps to those pages and scrapes their contence into a
        scrapy.item CCrecord
        :param response:
        :return: yields a record of a bunch of records
        """
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
            record_number = response.xpath(RECORD_NUMBER_XPATH).re('[.0-9]+')[0]
            # self.log(response.meta['pin'])
            yield scrapy.Request(url=DOCUMENTS_PAGE_URL + record_number + '/',
                                 callback=self.parse_docs_page,
                                 meta={
                                     'pin':response.meta['pin'],
                                     'record_number': record_number
                                    }
                                 )

    def parse_docs_page(self, response):
        """
        Parces the docs page of a pin after jumping to it.
        :param response - the downloaded record/docs page
        :return: yield a scrapy.item CCrecord for every valid PIN
        """
        record = CCrecord()
        record['pin'] = response.meta['pin']
        record['record_number'] = response.meta['record_number']
        self.log('Reached this point')
        yield record

'''
scrapy shell -s USER_AGENT="Mozilla/5.0" 
.re('[.0-9]+')
'''