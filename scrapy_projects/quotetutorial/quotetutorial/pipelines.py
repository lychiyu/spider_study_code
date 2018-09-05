# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class QuotetutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    """
    将item存储到mongodb
    """

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置文件中的消息
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        # spider开始时调用
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # 处理item insert to mongodb
        self.db['quotes'].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        # spider结束时调用
        self.client.close()
