# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider

from py3_crawler.items import AnjukeNewHouseItem, AnjukeSecondhandHouseItem

meta_proxy = "http://101.132.149.193:8080"


class AnjukeNewHouseSpider(Spider):
    name = 'anjuke_xinfang'

    headers = {
        ':authority': 'hz.fang.anjuke.com',
        ':method': 'GET',
        ':path': '/',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'sessid=18F4B1C5-114B-2FF9-37F4-AB3EFA6C3484; aQQ_ajkguid=FA7B5777-55BD-B8AF-70C8-B7F9FC6A9E0D; lps=http%3A%2F%2Fsjz.anjuke.com%2F%7C; ctid=28; twe=2; isp=true',
        'referer': 'https://hz.fang.anjuke.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://hz.fang.anjuke.com/'
        # yield Request(url, headers=self.headers)
        yield Request(url, headers=self.headers, meta={'proxy': meta_proxy})

    def parse(self, response):
        item = AnjukeNewHouseItem()
        houses = response.xpath("//div[contains(@class, 'key-list')]/div")
        for house in houses:
            item['name'] = house.xpath(".//a[@class='lp-name']//span/text()").extract_first()
            item['district'] = house.xpath(".//a[@class='address']/span/text()").extract_first().split()[1]
            item['bizcircle'] = house.xpath(".//a[@class='address']/span/text()").extract_first().split()[2]
            item['address'] = house.xpath(".//a[@class='address']/span/text()").extract_first().split()[4]
            huxing_list = house.xpath(".//a[@class='huxing']//span/text()").extract()
            if len(huxing_list) == 1:
                item['area'] = huxing_list[0]
            elif len(huxing_list) > 1:
                item['design'] = '/'.join(huxing_list[:-1])
                item['area'] = huxing_list[-1]
            item['status'] = house.xpath(".//a[@class='tags-wrap']//i[contains(@class, 'sale')]/text()").extract_first()
            item['type'] = house.xpath(".//a[@class='tags-wrap']//i[contains(@class, 'wuyetp')]/text()").extract_first()
            item['tags'] = ','.join(house.xpath(".//a[@class='tags-wrap']//span[@class='tag']/text()").extract())
            item['price'] = house.xpath(".//a[@class='favor-pos']/p[@class='price-txt']/text()").extract_first()
            item['tel'] = house.xpath(".//a[@class='favor-pos']/p[@class='tel']/text()").extract_first()
            yield item
        next_url = response.xpath('//a[contains(@class, "next-page")]//@href').extract_first()
        if next_url:
            # yield Request(next_url, headers=self.headers)
            yield Request(next_url, headers=self.headers, meta={'proxy': meta_proxy})


class AnjukeSecondhandHouseSpider(Spider):
    name = 'anjuke_ershoufang'

    headers = {
        ':authority': 'hangzhou.anjuke.com',
        ':method': 'GET',
        ':path': '/sale/',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://hangzhou.anjuke.com/sale/'
        # yield Request(url, headers=self.headers)
        yield Request(url, headers=self.headers, meta={'proxy': meta_proxy})

    def parse(self, response):
        # 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = AnjukeSecondhandHouseItem()
        houses = response.xpath("//ul[@id='houselist-mod-new']/li")
        for house in houses:
            item['name'] = house.xpath(".//div[@class='house-title']/a/text()").extract_first().strip()
            details_item = house.xpath(".//div[@class='details-item']/span/text()").extract()
            if len(details_item) >= 5:
                item['design'] = details_item[0]
                item['area'] = details_item[1]
                item['floor'] = details_item[2]
                item['year'] = details_item[3]
                item['district'] = details_item[4].split()[0].strip()
                item['address'] = details_item[4].split()[1].strip()
            item['tags'] = ','.join(house.xpath(".//div[@class='tags-bottom']/span/text()").extract())
            item['total_price'] = house.xpath(".//span[@class='price-det']/strong/text()").extract_first()
            item['unit_price'] = house.xpath(".//span[@class='unit-price']/text()").extract_first()
            yield item
        next_url = response.xpath('//a[contains(@class, "aNxt")]//@href').extract_first()
        if next_url:
            self.logger.info("Next URL: " + next_url)
            # yield Request(next_url, headers=self.headers)
            yield Request(next_url, headers=self.headers, meta={'proxy': meta_proxy})
