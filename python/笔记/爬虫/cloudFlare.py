# coding=utf-8
"""
用法类似requests
"""
# pip install cloudscraper
url = ""
import cloudscraper
scraper = cloudscraper.create_scraper()
resp = scraper.get(url).text
print(resp)


from lxml.html import fromstring
scraper = cloudscraper.create_scraper()
resp = scraper.get(url).text
selector = fromstring(resp)
title = selector.xpath('//h1/text()')[0]
print(title)


# pip install cfscrape
# 需要nodejs
import cfscrape
# 实例化一个create_scraper对象
scraper = cfscrape.create_scraper()
# 请求报错，可以加上时延
# scraper = cfscrape.create_scraper(delay = 10)

# 处理 get 请求的 CloudFlare

# 获取网页源代码
web_data = scraper.get("https://wallhere.com/").content
print(web_data)

# 处理 post 请求的 CloudFlare

# import cfscrape
# 实例化一个create_scraper对象
scraper = cfscrape.create_scraper()
# 获取真实网页源代码
web_data = scraper.post("http://example.com").content
print(web_data)