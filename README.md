# Scraping Cryptocurrencies Historical Data

This is a web crawler using Scrapy to scrape histiorical data of different cryptocurrency available on [CoinMarketCap](https://coinmarketcap.com). It is always tricky to scrapy the website at scale as one might experience IP banning which is also the case for this particular website. One good way to overcome this is by setting up the Scrapy to rotate proxies. However finding some free and working proxies are quite time consuming so I decide not to over-engineer the code since I am only interesting to get the whole historical data from just few cryptocurriencies. Hence the crawler is coded in such a way that only one particular cryptocurrency’s historical data will be scraped at a time given its ticker name and the time frame (starting date and ending date).  

## Dealing with JSON response with Scrapy

The data on this [website](https://coinmarketcap.com) is saved as a JSON object and is acessible through this HTML tag: `<script id="__NEXT_DATA__" type="application/json”>`. To extract the data I want from this JSON response, I am using the the Scrapy built in **ItemLoader** and **jmespath** as proposed by [Szabolcs Antal](https://robustify.wordpress.com/2017/12/22/how-to-scrape-json-response-with-scrapy-using-the-selectjmes-processor/). This is a clear-cut way to parse the JSON object using the **SelectJmes** processors and populate the Scrapy Item using its **ItemLoader**. Note that Scrapy doesn’t accept a DataFrame object to be populated.  

## How to use: 

+ Three user inputs are required to run the script: the sticker of the Cryptocurrency, Start Date and End Date. 
  + the user defined arguments are passed in the `crawl` command using the `-a` option
  + output of the `CSV` file can be passed using the `-o` option
+ Set up the scrapy project/clone this project and navigate to the directory of the project to run the following:
  + Example 1: to scrape Bitcoin’s historical data: `scrapy crawl crypto_spider -a ticker=BTC -a start='20130101' -a end="20201213" -o BTC.csv'
  +  Example 2: to scrape Etherum’s historical data: `scrapy crawl crypto_spider -a ticker=ETH -a start='20140101' -a end="20201213" -o ETH.csv`
+ the output CSV file (e.g.`BTC.csv / ETH.csv`) will be generated at the project directory

### References:

https://robustify.wordpress.com/2017/12/22/how-to-scrape-json-response-with-scrapy-using-the-selectjmes-processor/

https://github.com/TeamHG-Memex/scrapy-rotating-proxies

https://blog.scrapinghub.com/scrapy-proxy

https://www.scraperapi.com/blog/best-10-free-proxies-and-free-proxy-lists-for-web-scraping/

