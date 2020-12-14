# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptoItem(scrapy.Item):
    # define the fields for your item here like:
    Date = scrapy.Field()
    Open = scrapy.Field()
    High = scrapy.Field()
    Low = scrapy.Field()
    Close = scrapy.Field()
    Volume = scrapy.Field()
    Market_cap = scrapy.Field()
    Name = scrapy.Field()
    Ticker = scrapy.Field()
