# -*- coding: utf-8 -*-
import scrapy

from ..items import QuotetutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 默认的回调 response就是start_urls的响应
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotetutorialItem()
            content = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            item['content'] = content
            item['author'] = author
            item['tags'] = tags
            yield item
        # 获取下一页的链接
        next = response.css('.pager .next a::attr(href)').extract_first()
        next_url = response.urljoin(next)
        yield scrapy.Request(url=next_url, callback=self.parse)
