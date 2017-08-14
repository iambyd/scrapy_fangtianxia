# -*- coding: utf-8 -*-
import scrapy
from ..items import FangtianxiaItem
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')
start_url_data = pd.read_csv(
    '/Users/snowbing/Desktop/爬虫/fangtianxia/fangtianxia_html/data_start_url.csv', header=0)


class FangSpiderSpider(scrapy.Spider):
    """
    def __init__(self):
        super(FangSpiderSpider, self).__init__()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    """
    name = 'fang_spider'
    allowed_domains = ['fangjia.fang.com']
    start_urls = ['http://fangjia.fang.com/pghouse-c0sh/a025-b01646-h315/',
                  'http://fangjia.fang.com/pghouse-c0sh/a025-b01639-h315/'
                  ]
    # http://fangjia.fang.com/pghouse-c0sh/a025-b01646-h315-i32/
    # http://fangjia.fang.com/pghouse-c0sh/a025-b01646-h315-i33/
    # http://fangjia.fang.com/pghouse-c0sh/a025-b01646-h315-i34/
    #start_urls = start_url_data['start_url'].tolist()

    def parse(self, response):
        sel = Selector(response)
        fang_list = sel.xpath('//div[@class="list"]/div')
        k = 0
        l = 0
        for fang in fang_list:
            fangtianxiaitem = FangtianxiaItem()
            fangtianxiaitem['start_url'] = response.url
            fangtianxiaitem['city'] = u'上海'
            title = fang.xpath(
                '//span[@class="housetitle"]/a[@target="_blank"]/text()').extract()[l + k].strip()
            if len(title) < 1:
                l += 1
                title = fang.xpath(
                    '//span[@class="housetitle"]/a[@target="_blank"]/text()').extract()[l + k].strip()
                fangtianxiaitem['title'] = title
            else:
                fangtianxiaitem['title'] = title
            new_old = fang.xpath('//span[@class="housetitle"]').extract()[k]
            fangtianxiaitem['title_url'] = "http://fangjia.fang.com" + fang.xpath(
                '//span[@class="housetitle"]/a[@target="_blank"]/@href').extract()[k]
            if 'newhouseText' not in new_old:
                fangtianxiaitem['new_old'] = 'old'
            else:
                fangtianxiaitem['new_old'] = 'new'
            fangtianxiaitem['address'] = fang.xpath(
                '//p[@class="mt8"]/span[@class="pl5"]/@title').extract()[k].strip()
            # 爬取价格单位
            price_1 = fang.xpath('//div[@class="house"]/dl').extract()[k]
            text = Selector(text=price_1).xpath(
                '//dl/dd[@class="money mt30"]').extract_first()
            # 将价格和单位拼接
            fangtianxiaitem['price'] = fang.xpath(
                '//span[@class="price"]/text()').extract()[k].strip() + Selector(text=text).xpath(
                '//a/text()').extract()[1].strip()

            yield fangtianxiaitem
            k += 1
        url_list = sel.xpath(
            '//div/p[@class="pages floatr"]//a/@href').extract()
        if not url_list:
            print response.body
            exit()
        next_url = "http://fangjia.fang.com" + url_list[len(url_list) - 1]
        # print 'aaaaaaaaaa', next_url
        yield scrapy.Request(next_url, self.parse)
