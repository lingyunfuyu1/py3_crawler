# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random
import telnetlib

import requests
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)

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

    def __init__(self):
        try:
            # 从https://www.xicidaili.com/获取代理
            logger.info('Getting proxies from https://www.xicidaili.com/ ...')
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
            soup = BeautifulSoup(response.text, 'html.parser')
            trs = soup.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                if len(tds) < 8:
                    continue
                if tds[5].string.lower() not in ['http', 'https']:
                    continue
                ProxyMiddleware.proxy_list.append(tds[5].string.lower() + '://' + tds[1].string + ':' + tds[2].string)
        except:
            logger.info('Exception occurd when getting proxies from https://www.xicidaili.com/')
        try:
            # 从http://www.xiladaili.com/获取代理
            logger.info('Getting proxies from https://www.xiladaili.com/ ...')
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                # 'Cookie': 'Hm_lvt_e556949542df6146a3d727d8ad4a49e6=1562655394; Hm_lpvt_e556949542df6146a3d727d8ad4a49e6=1562655394',
                'Host': 'www.xiladaili.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            }
            response = requests.get('http://www.xiladaili.com/', headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            trs = soup.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                if len(tds) < 8:
                    continue
                protocol = tds[2].string.lower()
                if protocol not in ['http', 'https', 'http,https']:
                    continue
                if protocol.find(',') != -1:
                    protocol = protocol.split(',')[0]
                ProxyMiddleware.proxy_list.append(protocol + '://' + tds[0].string)
        except:
            logger.info('Exception occurd when getting proxies from http://www.xiladaili.com/')
        # 统计获取的代理
        if not ProxyMiddleware.proxy_list:
            logger.info('Failed to get any proxy!')
        else:
            logger.info('Successfully got ' + str(len(ProxyMiddleware.proxy_list)) + ' proxies.')

    @staticmethod
    def process_request(request, spider):
        while True:
            # 手工设置禁用proxy
            if request.meta.get('disable_proxy', False):
                # if 'proxy' in request.meta:
                #     del request.meta['proxy']
                return
            # 手工设置的proxy优先
            if 'proxy' in request.meta:
                return
            if not ProxyMiddleware.proxy_list:
                raise NoAvailableProxy
            # 随机选择
            # proxy = random.choice(ProxyMiddleware.proxy_list)
            # 依次使用
            proxy = ProxyMiddleware.proxy_list[0]
            ip = proxy.split('//')[-1].split(':')[0]
            port = proxy.split('//')[-1].split(':')[1]
            max_check_times = 3
            for i in range(max_check_times):
                try:
                    telnetlib.Telnet(ip, port=port, timeout=3)
                except:
                    if i + 1 >= max_check_times:
                        ProxyMiddleware.proxy_list.remove(proxy)
                        logger.info('Remove proxy due to Telnet-Error: %s [%s remaining]' % (proxy, str(len(ProxyMiddleware.proxy_list))))
                else:
                    request.meta['proxy'] = proxy
                    return


class XHRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        logger.info('[' + str(response.status) + '] ' + response.url + ' proxy:' + str(request.meta.get('proxy', '')))
        if request.meta.get('dont_retry', False):
            logger.info("request.meta.get('dont_retry') is set to 'True'. No need to retry.")
            return response
        proxy = request.meta.get('proxy', None)
        if response.status in [403, 404] and proxy in ProxyMiddleware.proxy_list:
            logger.info('Remove proxy due to Http-Error: %s [%s]' % (proxy, str(len(ProxyMiddleware.proxy_list))))
            ProxyMiddleware.proxy_list.remove(proxy)
        if response.status in self.retry_http_codes:
            logger.info("Retry from XHRetryMiddleware.process_response: " + request.url)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        logger.info('[' + str(exception) + '] ' + request.url + ' proxy:' + str(request.meta.get('proxy', '')))
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            logger.info("Retry from XHRetryMiddleware.process_exception: " + request.url)
            return self._retry(request, exception, spider)


class NoAvailableProxy(Exception):
    pass