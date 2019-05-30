# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CCrecordLineName(scrapy.Item):
    """doc1_table item
    """
    name = scrapy.Field()
    type = scrapy.Field()


class CCrecordLineParcel(scrapy.Item):
    """doc2_table item
    """
    pin = scrapy.Field()
    address = scrapy.Field()


class CCrecordLineRelatedDoc(scrapy.Item):
    """doc3_table item
    """
    doc_number = scrapy.Field()
    url = scrapy.Field()


class CCrecordLine(scrapy.Item):
    """
    A single line in a list of documents of a record
    """
    date = scrapy.Field()
    doc_type = scrapy.Field()
    doc_num = scrapy.Field()
    consideration = scrapy.Field()
    names = scrapy.Field()
    parcels = scrapy.Field()
    related_docs = scrapy.Field()
    show_doc = scrapy.Field()


class CCrecord(scrapy.Item):
    """
    The complete record/list of events associated with a PIN
    """
    pin = scrapy.Field()
    record_number = scrapy.Field()
    lines = scrapy.Field()

    '''
    def __init__(self):
        """
        initialize lines as an empty dictionary
        """
        lines = {}
        return
    '''
