# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider

from py3_crawler.items import LianjiaCommunityItem


class LianjiaXiaoquSpider(Spider):
    name = 'lianjia_xiaoqu'
    count = 0
    xiaoqu_count = 0
    detail_count = 0

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'TY_SESSION_ID=26af4dc6-aea3-4977-9ab8-c7d178f1818f; select_city=330100; all-lj=979909237fcf62bcb16b5a6dbd3b060f; lianjia_ssid=619de8d4-1fe6-43ee-a1b3-62c7d9fa771f; lianjia_uuid=d558b963-d3b1-4165-9278-5a9a3cecfd83; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1559800592; _smt_uid=5cf8ab10.137619af; UM_distinctid=16b2b5c39fd10b-0b5ccd4fe2edf9-19106221-fa000-16b2b5c39fe40d; CNZZDATA1253492436=976263998-1559799488-%7C1559799488; CNZZDATA1254525948=1791097797-1559797658-%7C1559797658; CNZZDATA1255633284=956946806-1559799008-%7C1559799008; CNZZDATA1255604082=1378687027-1559798298-%7C1559798298; _jzqa=1.941456631128820900.1559800593.1559800593.1559800593.1; _jzqc=1; _jzqckmp=1; _qzjc=1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b2b5c3f37313-02ba722a2aed39-19106221-1024000-16b2b5c3f38489%22%2C%22%24device_id%22%3A%2216b2b5c3f37313-02ba722a2aed39-19106221-1024000-16b2b5c3f38489%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.2.2026562402.1559800596; _gid=GA1.2.490736752.1559800596; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1559800619; _qzja=1.1740922854.1559800593525.1559800593525.1559800593526.1559800593526.1559800619371.0.0.0.2.1; _qzjb=1.1559800593526.2.0.0.0; _qzjto=2.1.0; _jzqb=1.2.10.1559800593.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTA3YWU1NTE3ZDMzNzc4NWY2YTljMjc1ODk4NzRiODNiOTAzODk5ODcwMmUzMDY3YjY2ODIyM2Y5NThjN2RlMzQ3NmIyMTk2ZDlkOWRiNWY5YmZjMmRkOGI2MzJjMDYwNjUxMmIxMWZmNjQ5NzM0MTNlZThlYjA2ZGI2Y2M0ZThiNzFkNTM2MTdhMjJhM2QyYjU3OTk3ZWY2NzZkYzYxNTUxMzc0ZWU1ZTQ3OTY5ZDM2ODBlNzhlOTQ0ZDg2ZWRmODg1N2QxYmYzZTJhZTZiYWVmZjYxZTk2NGM5NDE3ZjIyNjkwMTczOTU2Y2Y5NjMyZjQ4ZWJjZGFlZGEyMzMyNWMzZDg5OGJjNjEzZmYxZDI4NjFkNjlkYTZkZjNmNWExXCIsXCJrZXlfaWRcIjpcIjFcIixcInNpZ25cIjpcImRiZjMxYWE3XCJ9IiwiciI6Imh0dHBzOi8vaHoubGlhbmppYS5jb20veGlhb3F1L3BnMjl5MXkyLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9',
        'Host': 'hz.lianjia.com',
        'Referer': 'https://hz.lianjia.com/xiaoqu/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    }

    def start_requests(self):
        for page_number in range(1, 50):
            url = 'https://hz.lianjia.com/xiaoqu/pg%sy1y2/' % str(page_number)
            yield Request(url, headers=self.headers)

    def parse(self, response):
        communities = response.xpath("//ul[@class='listContent']/li")
        self.count += 1
        self.xiaoqu_count += len(communities)
        self.logger.info('[' + str(self.count) + ']: ' + str(len(communities)) + ', total: ' + str(self.xiaoqu_count))
        for community in communities:
            community_id = community.xpath('.//@data-id').extract_first()
            if not community_id:
                self.logger.error('Missing Community ID! community: ' + community)
            introduce_url = 'https://hz.lianjia.com/xiaoqu/%s/' % community_id
            self.logger.info('Detail URL: ' + introduce_url)
            yield Request(introduce_url, headers=self.headers, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = LianjiaCommunityItem()
        item['community'] = response.xpath('//h1/text()').extract_first()
        item['district'] = response.xpath('//div[@class="xiaoquDetailbreadCrumbs"]/div[1]/a[3]/text()').extract_first()
        item['bizcircle'] = response.xpath('//div[@class="xiaoquDetailbreadCrumbs"]/div[1]/a[4]/text()').extract_first()
        item['avg_unit_price'] = response.xpath('//span[@class="xiaoquUnitPrice"]/text()').extract_first()
        item['jznd'] = response.xpath('//div[@class="xiaoquInfo"]/div[1]/span[2]/text()').extract_first()
        item['jzlx'] = response.xpath('//div[@class="xiaoquInfo"]/div[2]/span[2]/text()').extract_first()
        item['wyfy'] = response.xpath('//div[@class="xiaoquInfo"]/div[3]/span[2]/text()').extract_first()
        item['wygs'] = response.xpath('//div[@class="xiaoquInfo"]/div[4]/span[2]/text()').extract_first()
        item['kfs'] = response.xpath('//div[@class="xiaoquInfo"]/div[5]/span[2]/text()').extract_first()
        item['ldzs'] = response.xpath('//div[@class="xiaoquInfo"]/div[6]/span[2]/text()').extract_first()
        item['fwzs'] = response.xpath('//div[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract_first()
        yield item
