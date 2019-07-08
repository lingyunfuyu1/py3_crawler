# -*- coding: utf-8 -*-

import json
import re
import time

from scrapy import Request
from scrapy.spiders import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from py3_crawler.items import DoubanMovieItem


class DoubanMovieTop250Spider(Spider):
    name = 'douban_movie_top250'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        # 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = DoubanMovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(r'(\d+)人评价')[0]
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            print('++++ next_url', next_url)
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers)


class DoubanAJAXSpider(Spider):
    name = 'douban_ajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        datas = json.loads(response.body)
        item = DoubanMovieItem()
        if datas:
            for data in datas:
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['score'] = data['score']
                item['score_num'] = data['vote_count']
                yield item

            # 如果datas存在数据则对下一页进行采集
            page_num = re.search(r'start=(\d+)', response.url).group(1)
            page_num = 'start=' + str(int(page_num) + 20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield Request(next_url, headers=self.headers)


class DoubanFavoriteSpider(Spider):
    name = 'douban_favorite'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        # 大陆
        url = 'https://movie.douban.com/tag/#/?sort=S&range=6,10&tags=%E7%94%B5%E5%BD%B1,%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86'
        # 香港
        # url = 'https://movie.douban.com/tag/#/?sort=S&range=6,10&tags=%E7%94%B5%E5%BD%B1,%E9%A6%99%E6%B8%AF'
        # 台湾
        # url = 'https://movie.douban.com/tag/#/?sort=S&range=6,10&tags=%E7%94%B5%E5%BD%B1,%E5%8F%B0%E6%B9%BE'
        driver.get(url)
        # 点击加载更多，直到全部加载完成
        a_more = 'pre-defined'
        while a_more:
            try:
                a_more = driver.find_element_by_class_name('more')
                a_more.click()
                time.sleep(3)
            except NoSuchElementException:
                a_more = ''
        # 获取电影链接
        element_list = driver.find_element_by_class_name('list-wp').find_elements_by_tag_name('a')
        for i in range(len(element_list)):
            url = element_list[i].get_attribute('href')
            yield Request(url, headers=self.headers)

    def parse(self, response):
        # 命令行调试代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = DoubanMovieItem()
        movie = response.xpath('//div[@id="content"]')
        item['movie_name'] = movie.xpath('.//h1/span[1]/text()').extract()[0]
        item['year'] = movie.xpath('.//h1/span[2]/text()').extract()[0].replace('(', '').replace(')', '')
        item['director'] = '/'.join(movie.xpath('.//span[contains(text(), "导演")]/following-sibling::*[1]/a/text()').extract())
        item['screenwriter'] = '/'.join(movie.xpath('.//span[contains(text(), "编剧")]/following-sibling::*[1]/a/text()').extract())
        item['leading_actors'] = '/'.join(movie.xpath('.//span[contains(text(), "主演")]/following-sibling::*[1]/a/text()').extract())
        item['type'] = '/'.join(movie.xpath('.//span[contains(text(), "类型")]/following-sibling::*[1]/a/text()').extract())
        item['score'] = movie.xpath('.//strong[contains(@class, "rating_num")]/text()').extract_first()
        item['score_num'] = movie.xpath('.//a[@class="rating_people"]/span/text()').extract_first()
        yield item
