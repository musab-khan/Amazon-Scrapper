# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonScrapItem

class FirstSpider(scrapy.Spider):
    name = 'first'
    start_urls = [
        'https://www.amazon.com/s?i=videogames-intl-ship&rh=n%3A%2116225016011&page=1&qid=1583650513&ref=lp_16225016011_pg_2'
    ]
    page1 = True
    # def parse_category(self, response):
    #     categories = response.css('.browseBox a::attr(href)').getall()
    #
    #     temp = categories[2:]
    #
    #     for category in temp:
    #         self.flag = True
    #         yield scrapy.Request(response.urljoin(category), callback=self.parse)

    def parse(self, response):
        item = AmazonScrapItem()

        if self.page1:
            products = response.css('.s-result-item')

            for product in products:
                name = product.css('.s-access-title::text').get()

                if product.css('.a-offscreen') is not None:
                    price = product.css('.a-offscreen::text').get()
                else:
                    price = product.css('.a-color-base::text').get()

                stars = product.css('.a-icon-alt::text').get()
                image = product.css('.cfMarker::attr(src)').get()

                item['product_name'] = name
                item['product_price'] = price
                item['product_image'] = image
                item['product_stars'] = stars

                yield item

        else:
            products = response.css('.s-include-content-margin')

            for product in products:
                name = product.css('.a-color-base.a-text-normal::text').get()

                if product.css('.a-offscreen') is not None:
                    price = product.css('.a-offscreen::text').get()
                else:
                    price = product.css('.a-color-base::text').get()

                image = product.css('.s-image::attr(src)').get()
                stars = product.css('.a-icon-alt::text').get()

                item['product_name'] = name
                item['product_price'] = price
                item['product_image'] = image
                item['product_stars'] = stars[:3]

                yield item


        if self.page1:
            next_page = response.css('.pagnRA a::attr(href)').get()
            self.page1 = False
        else:
            next_page = response.css('.a-last a::attr(href)').get()

        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)