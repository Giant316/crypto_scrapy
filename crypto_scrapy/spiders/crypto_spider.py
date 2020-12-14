import scrapy
import json
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, SelectJmes
from crypto_scrapy.items import CryptoItem
import sys 
from datetime import datetime

class CryptoSpiderSpider(scrapy.Spider):
	name = 'crypto_spider'
	allowed_domains = ['coinmarketcap.com']
	start_urls = ['http://coinmarketcap.com']
	# dictionary to map the class CryptoItem in items.py to Jmes query paths
	jmes_paths = {
			"Date": 'quote.USD.["timestamp"]',
			"Open": 'quote.USD.["open"]',
			"High": 'quote.USD.["high"]',
			"Low": 'quote.USD.["low"]',
			"Close": 'quote.USD.["close"]',
			"Volume": 'quote.USD.["volume"]',
			"Market_cap": 'quote.USD.["market_cap"]'
		}
	def __init__(self,ticker='',start='', end='', *args,**kwargs):
		# to get user input from the console, override the original __init__
		super(CryptoSpiderSpider, self).__init__(*args, **kwargs)
		self.ticker = ticker
		self.start = start
		self.end = end

	def validate_date(self):
		try:
			if (len(self.start) == 8) & (len(self.end) == 8):
				if (datetime.strptime(self.end, '%Y%m%d') > datetime.strptime(self.start, '%Y%m%d')):
					return True
				else: raise ValueError("Start Date > End Date!")
			elif (self.start == '') | (self.end == ''): raise ValueError("Please provide date(s) input!")
			else: raise ValueError("Invalid Date(s)!")
		except ValueError:
			raise ValueError("Invalid Date(s)!")

	def validate_ticker(self, lookup):
		try:
			if (self.ticker in lookup):
				return True
		except ValueError:
			raise ValueError("Invalid Ticker!")

	def parse(self,response):
		# extract the json response from the tag: <script id="__NEXT_DATA__" type="application/json”>
		jsonresponse = json.loads(response.css('#__NEXT_DATA__::text').extract()[0])
		# retrieve the list of all available cryptocurriencies on the first page 
		data = jsonresponse['props']['initialState']['cryptocurrency']['listingLatest']['data']
		# save all available cryptocurriencies in a dictionary 
		lookup = {}
		for idx, val in enumerate(data):
			lookup[val['symbol']] = {'name': val['name'], 'idx': idx}

		hrefs = list(dict.fromkeys(response.css('td > a::attr(href)').extract()))
		urls = [self.start_urls[0] + x + 'historical-data/' for x in hrefs]
		
		# validate the user inputs 
		if(self.validate_ticker(lookup)) & (self.validate_date()):
			# construct a valid url to make a request 
			url = urls[lookup[self.ticker]['idx']] + '?start=' + self.start + '&end=' + self.end
			yield scrapy.Request(url = url, callback = self.parse_page)

	def parse_page(self, response):
		# extract the json response from the tag: <script id="__NEXT_DATA__" type="application/json”>
		jsonresponse = json.loads(response.css('#__NEXT_DATA__::text').extract()[0])
		# access the historical data within the JSON object 
		nestedJson = jsonresponse['props']['initialState']['cryptocurrency']['ohlcvHistorical']
		# retrieve the id of the crypto (a key value)
		id = [str(k) for k in nestedJson.keys()][0]
		# get the name of the respective crypto 
		name = nestedJson[id]['name']
		# save the ticker symbol 
		ticker = jsonresponse['props']['initialState']['cryptocurrency']['ohlcvHistorical'][id]['symbol']
		# accesss the historical data: e.g. Open, Close, High, Low, etc. 
		data = jsonresponse['props']['initialState']['cryptocurrency']['ohlcvHistorical'][id]['quotes']
		for d in data: 
			loader = ItemLoader(item=CryptoItem())
			loader.default_input_processor = MapCompose(str)
			loader.default_ouput_processor = Join('')

			for (field, path) in self.jmes_paths.items():
				loader.add_value(field, SelectJmes(path)(d))
			loader.add_value("Name", name)
			loader.add_value("Ticker", ticker)

			yield loader.load_item()
		