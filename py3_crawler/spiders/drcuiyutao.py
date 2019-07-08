# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request


class DrcuiyutaoSpider(scrapy.Spider):
    name = "drcuiyutao"

    def start_requests(self):
        # url = 'http://m.drcuiyutao.com/yxy-babyhealth-wap/knowlege/findbyid.htm?knId=777'
        url = 'http://m.drcuiyutao.com/yxy-babyhealth-wap/knowlege/findbyid.htm?knId=239'
        yield Request(url)

    def parse(self, response):
        for section in response.xpath("//section[@class='article-item']"):
            coup_detail_url = 'http://m.drcuiyutao.com' + section.xpath(
                ".//a[contains(@href, 'coup_detail')]/@href").extract_first()
            yield Request(coup_detail_url, self.parse_coup)
        next_page = response.xpath(
            "//div[@class='sec-tip']//div[@class='pages']//span[@class='next']/..//@href").extract_first()
        if next_page:
            yield response.follow('http://m.drcuiyutao.com' + next_page, self.parse)

    def parse_coup(self, response):
        coup = response.meta.get('coup')
        if not coup:
            article = response.xpath("//article[contains(@class, 'article-knowledge')]")
            coup = {
                'author': article.xpath(".//h3/text()").extract_first(),
                'time': article.xpath(".//p[contains(text(), '发布于')]/text()").extract_first(),
                'content': article.xpath('.//article/p/text()').extract_first(),
                'comms': [],
                'comm_count': 0
            }
            if not coup.get('author'):
                self.logger.info('获取用户名失败，使用默认值')
                coup['author'] = '未知用户'
        for comm in response.xpath("//ul[@class='comm-list']/li"):
            comm = {
                'author': comm.xpath(".//h3/a/text()").extract_first(),
                'time': comm.xpath(".//time/text()").extract_first(),
                'content': comm.xpath('.//p/text()').extract_first(),
            }
            coup.get('comms').append(comm)
            coup['comm_count'] = len(coup.get('comms'))
        next_page = response.xpath(
            "//div[@class='sec-dis']//div[@class='pages']//span[@class='next']/..//@href").extract_first()
        if next_page:
            yield Request('http://m.drcuiyutao.com' + next_page, callback=self.parse_coup, meta={'coup': coup})
        else:
            result_file = open('data/result/drcuiyutao.txt', 'a')
            result_file.write('-' * 50 + '\n')
            result_file.write(coup.get('author').strip().replace('\r\n', '').replace('\n', '') + ' ' + coup.get('time').strip().replace('\r\n', '').replace('\n', '') + '\n')
            result_file.write('【帖子】\n')
            result_file.write(coup.get('content').strip().replace('\r\n', '').replace('\n', '') + '\n')
            result_file.write('【评论】\n')
            for comm in coup.get('comms'):
                result_file.write(comm.get('time').strip().replace('\r\n', '').replace('\n', '') + '|' + comm.get('author').strip().replace('\r\n', '').replace('\n', '') + ': ' + comm.get('content').strip().replace('\r\n', '').replace('\n', ''))
                result_file.write('\n')
            result_file.write('\n')
            result_file.close()
            yield coup
