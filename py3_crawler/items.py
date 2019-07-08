# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Py3CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanMovieItem(scrapy.Item):
    # ID
    id = scrapy.Field()
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 年份
    year = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 编剧
    screenwriter = scrapy.Field()
    # 主演
    leading_actors = scrapy.Field()
    # 类型
    type = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()


class AnjukeNewHouseItem(scrapy.Item):
    name = scrapy.Field()
    district = scrapy.Field()
    bizcircle = scrapy.Field()
    address = scrapy.Field()
    design = scrapy.Field()
    area = scrapy.Field()
    status = scrapy.Field()
    type = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    tel = scrapy.Field()


class AnjukeSecondhandHouseItem(scrapy.Item):
    name = scrapy.Field()
    design = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    year = scrapy.Field()
    district = scrapy.Field()
    address = scrapy.Field()
    tags = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()


class LianjiaHouseItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    sign_date = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()


class LianjiaCommunityItem(scrapy.Item):
    # 唯一ID
    id = scrapy.Field()
    # 小区
    community = scrapy.Field()
    # 区域
    district = scrapy.Field()
    # 商圈
    bizcircle = scrapy.Field()
    # 建成年份
    building_finish_year = scrapy.Field()
    # 均价（上月？）
    avg_unit_price = scrapy.Field()
    # 成交数量（90天）
    sale_count = scrapy.Field()
    # 在售数量
    source_count = scrapy.Field()
    # 建筑年代
    jznd = scrapy.Field()
    # 建筑类型
    jzlx = scrapy.Field()
    # 物业费用
    wyfy = scrapy.Field()
    # 物业公司
    wygs = scrapy.Field()
    # 开发商
    kfs = scrapy.Field()
    # 楼栋总数
    ldzs = scrapy.Field()
    # 房屋总数
    fwzs = scrapy.Field()
