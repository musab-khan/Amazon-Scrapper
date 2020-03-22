# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonScrapItem


class SecondSpider(scrapy.Spider):
    name = 'second'
    start_urls = [
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=4954955011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=2562090011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225005011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225006011',
        'https://www.amazon.com/s?ie=UTF8&bbn=283155&rh=i%3Astripbooks%2Cn%3A283155%2Cp_n_availability%3A2245265011%2Cp_n_shipping_option-bin%3A3242350011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225007011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225009011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225018011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225019011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225020011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225021011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225010011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225011011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225012011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225017011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=2625373011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=5174',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225013011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225008011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225014011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=256643011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225015011',
        'https://www.amazon.com/b?_encoding=UTF8&ie=UTF8&node=16225016011'
    ]

    def parse(self, response):
        item = AmazonScrapItem()

        products = response.css('.s-result-item')

        for product in products:
            name    =   product.css('.s-access-title::text').get() or product.css('.a-color-base.a-text-normal::text').get()
            price   =   product.css('.a-offscreen::text').get() or product.css('.a-color-base::text').get()
            stars   =   product.css('.a-icon-alt::text').get()
            image   =   product.css('.cfMarker::attr(src)').get() or product.css('.s-image::attr(src)').get()
            asin    =   product.css('::attr(data-asin)').get()

            item['product_name']    = name
            item['product_price']   = price
            item['product_image']   = image
            item['product_stars']   = stars.split(' ')[0] if stars is not None else "N/A"
            item['product_asin']    = asin

            yield item

        next_page = response.css('.pagnRA a::attr(href)').get() or response.css('.a-last a::attr(href)').get()

        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)

