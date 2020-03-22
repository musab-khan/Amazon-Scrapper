# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import boto3

class AmazonScrapPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb+srv://musab:ragga123@cluster0-4daes.mongodb.net/test?retryWrites=true&w=majority")
        db = self.conn['Amazon']
        self.collection = db['products']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class DynamoPipeline(object):

    def __init__(self):
        self.dynamo = boto3.resource('dynamodb', region_name="us-east-1")
        self.table = self.dynamo.Table('Products')

    def process_item(self, item, spider):
        self.table.put_item(Item={
            "ASIN": item["product_asin"],
            "Title": item["product_name"],
            "Image_URL": item["product_image"],
            "Price": item["product_price"],
            "Rating": item["product_stars"]
        })
        return item
