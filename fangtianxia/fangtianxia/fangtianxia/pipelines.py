# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from collections import OrderedDict
from scrapy.exceptions import DropItem


class FangtianxiaPipeline(object):

    def __init__(self):
        self.title_url_set = set()
        self.file1 = codecs.open('data.json', 'w', encoding='utf-8')
        self.file2 = codecs.open('data.csv', 'w', encoding='utf-8')
        self.fileheader = ['start_url', 'city',
                           'title', 'title_url', 'new_old', 'address', 'price']
        self.file2.write(";".join(self.fileheader) + '\n')

    def process_item(self, item, spider):
        # 去除重复数据
        if item['title_url'] in self.title_url_set:
            raise DropItem(u"重复记录: %s" % item)
        else:
            ITEM = dict(item)
            content = [ITEM['start_url'], ITEM['city'], ITEM['title'], ITEM['title_url'],
                       ITEM['new_old'], ITEM['address'], ITEM['price']]
            line1 = json.dumps(OrderedDict(
                zip(self.fileheader, content)), ensure_ascii=False)
            line2 = ",".join(content) + '\n'
            self.file1.write(line1 + '\n')
            self.file2.write(line2)
            self.title_url_set.add(item['title_url'])
            return item

    def spider_closed(self, spider):
        self.file1.close()
        self.file2.close()
