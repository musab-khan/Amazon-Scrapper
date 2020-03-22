# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class AmazonScrapPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient('mongodb+srv://musab:<password>@cluster0-4daes.mongodb.net/test?retryWrites=true&w=majority')
        db = self.conn['Ubuntu']
        self.collection = db['products']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
