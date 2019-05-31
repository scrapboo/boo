# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CSVFeedSpider
from ccrecorder.items import CCrecord, CCrecordLine, CCrecordLineName, CCrecordLineParcel, CCrecordLineRelatedDoc
import parsel


class RecordsSpider(CSVFeedSpider):
    """
    Reads the pin feed csv file and parses the CC recorder
    for these pins.
    The pins can be 10 or 14 digit long
    """
    name = 'records2'
    allowed_domains = ['ccrecorder.org']
    start_urls = ['https://alxfed.github.io/docs/pin_feed2.csv']
    headers = ['pin']

    def parse_row(self, response, row):
        """
        Reads a row in csv and makes a request to the pin page
        :param response: the downloaded pin page
        :param row: a single PIN read from the pin feed file
        :return: yields a scrapy.Request to pin page
        """
        PIN_REQUEST_URL = 'https://www.ccrecorder.org/parcels/search/parcel/result/?line='
        pin = row['pin']                                                # the name of the column defined in 'headers'
        yield scrapy.Request(url=PIN_REQUEST_URL + pin, callback=self.parse_pin_page, meta={'pin':pin})

    def parse_pin_page(self, response):
        """
        Parses the pin page, detects if there is none, detects if
        there are multiple pins and their corresponding links on a page,
        jumps to those pages and scrapes their contence into a
        scrapy.item CCrecord
        :param response:
        :return: yields a record or a bunch of records
        """
        DOCUMENTS_PAGE_URL = 'https://www.ccrecorder.org/parcels/show/parcel/'
        PIN_LIST_LINE_XPATH = '//*[@id="pins_table"]/*[@id="objs_body"]/tr'  #//*[@id="objs_table"]
        PIN14_XPATH = '/td[1]/text()'
        STREET_ADDRESS_XPATH = '/td[2]/text()'
        CITY_XPATH = '/td[3]/text()'
        RECORD_NUMBER_XPATH = '/td[4]/a/@href'
        NO_PINS_FOUND_RESPONSE_XPATH = '//html/body/div[4]/div/div/div[2]/div/div/p[2]/text()' # where it can be

        # And now...
        NOT_FOUND = response.xpath(NO_PINS_FOUND_RESPONSE_XPATH).get()  # what is there
        if NOT_FOUND:                                                   # ?  (can't do without this, because of None)
            if NOT_FOUND.startswith('No PINs'):                         # No PINs?
                # self.log('Not found PIN '+response.url)                 # Debug notification
                yield None                                              # and get out of here.

            else:
                self.log('something is in the place of No PINs but it is not it')
                yield None

        else:                                                           # there is a PIN like that
            # Tried to iterate over selectors but it didn's work, this is a less elegant way
            lines_list = response.xpath(PIN_LIST_LINE_XPATH).getall()
            # extract the number(s) for the record(s), jump
            # to the docs page (as many times as necessary, come back every time when done
            for index, line in enumerate(lines_list):  # not to forget that 14 digit PIN gives 2 tables of results.
                linear = str(index+1)
                line_xpath = '{}[{}]'.format(PIN_LIST_LINE_XPATH, linear)
                pin = response.xpath(line_xpath + PIN14_XPATH).get()
                street_address = response.xpath(line_xpath + STREET_ADDRESS_XPATH).get()
                city = response.xpath(line_xpath + CITY_XPATH).get().strip()             # strip removes trailing spaces
                record_number = response.xpath(line_xpath + RECORD_NUMBER_XPATH).re('[.0-9]+')[0]
                # self.log(response.meta['pin'])
                yield scrapy.Request(url=DOCUMENTS_PAGE_URL + record_number + '/',
                                 callback=self.parse_docs_page,
                                 meta={
                                     'pin': pin,
                                     'street_address': street_address,
                                     'city': city,
                                     'record_number': record_number
                                    }
                                 )


    def parse_docs_page(self, response):
        """
        Parces the docs page of a pin after jumping to it.
        :param response - the downloaded record/docs page
        :return: yield a scrapy.item CCrecord for every valid PIN
        """
        DOCS_TABLE_LINE_XPATH = '//*[@id="docs_body"]/tr'
        DOC_DATE_RECORDED_XPATH = '/td[1]/text()'
        DOC_TYPE_RECORDED_XPATH = '/td[2]/text()'
        DOC_NUM_RECORDED_XPATH = '/td[3]/text()'
        DOC_URL_NUM_XPATH = '/td[3]/a/@href/text()'
        DOC_CONSIDERATION_XPATH = 'td[4]/text()'
        DOCS1_TABLE_LINE_XPATH = '//*[@id="docs1_body"]/tr'

        record = CCrecord()
        record['lines'] = {}

        record['pin'] = response.meta['pin']
        record['street_address'] = response.meta['street_address']
        record['city'] = response.meta['city']
        record['record_number'] = response.meta['record_number']

        line = CCrecordLine()

        liness_list = response.xpath(DOCS_TABLE_LINE_XPATH).getall()

        for index, liness in enumerate(liness_list):  # not to forget that 14 digit PIN gives 2 tables of results.
            linearr = str(index + 1)
            line_xpath = '{}[{}]'.format(DOCS_TABLE_LINE_XPATH, linearr)
            line['index'] = index
            line['date'] = response.xpath(line_xpath + DOC_DATE_RECORDED_XPATH).get()
            line['doc_type'] = response.xpath(line_xpath + DOC_TYPE_RECORDED_XPATH).get()
            line['doc_num'] = response.xpath(line_xpath + DOC_NUM_RECORDED_XPATH).get()
            line['doc_url_num'] = response.xpath(line_xpath + DOC_URL_NUM_XPATH).get()   # extract the number
            line['consideration'] = response.xpath(line_xpath + DOC_CONSIDERATION_XPATH).get()

            linesss_list = response.xpath(line_xpath + DOCS1_TABLE_LINE_XPATH).getall()
            # for #1 name/type
            for indx, linesss in enumerate(linesss_list):
                linearrr = str(indx + 1)

        record['docs'].update(line)
        # self.log('Reached this point')
        yield record

'''
.re('[.0-9]+')
'''