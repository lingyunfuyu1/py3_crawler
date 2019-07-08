# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import telnetlib

import requests
from bs4 import BeautifulSoup
from scrapy import signals

from py3_crawler.settings import PROXIES


class Py3CrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Py3CrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    proxy_list = []

    def __init__(self, spider):
        try:

            spider.logger.info('Getting proxies from https://www.xicidaili.com/ ...')
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                # 'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTk1MWRkNWMwMzc5NTcwMmYxMGE3MTZkZTEzMTliZTc4BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUI5NXJ1ZmxOWG5ZM3lUR2tMWVk1eW9lMm1uakR5U0JYcTlUK25qNGRXZjg9BjsARg%3D%3D--6c734a7138e0a3804c29f05f15a333a49febd5ca; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1560753157,1562131188; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1562572697',
                'Host': 'www.xicidaili.com',
                # 'If-None-Match': 'W/"adc819458dfd329611ea0c5894199c48"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            }
            response = requests.get('https://www.xicidaili.com/', headers=headers)
            soup = BeautifulSoup(response.text)
            trs = soup.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                if len(tds) < 8:
                    continue
                ip = tds[1].string
                port = tds[2].string
                protocol = tds[5].string
                self.proxy_list.append((ip, port, protocol))
            if not self.proxy_list:
                spider.logger.info('Failed to get any proxy!')
            else:
                spider.logger.info('Successfully got ' + str(len(self.proxy_list)) + 'proxies.')
        except:
            spider.logger.info('Exception occurd when getting proxies!')

    def process_request(self, request, spider):
        while True:
            if not self.proxy_list:
                spider.logger.info('The proxy list is empty!')
                return
            proxy = random.choice(self.proxy_list)
            try:
                telnetlib.Telnet(proxy[0], port=proxy[1], timeout=3)
            except:
                self.proxy_list.remove(proxy)
                spider.logger.info('Removed proxy: %s' % str(proxy))
            else:
                request.meta['proxy'] = proxy



