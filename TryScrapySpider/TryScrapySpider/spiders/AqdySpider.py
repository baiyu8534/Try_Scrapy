# -*- coding: utf-8 -*-
import scrapy
from pprint import pprint
import logging
from TryScrapySpider.items import TryscrapyspiderItem
from copy import deepcopy

pre_url = "http://aqdyee.com"


class AqdyspiderSpider(scrapy.Spider):
    name = 'AqdySpider'
    allowed_domains = ['aqdyee.com']
    start_urls = ['http://aqdyee.com/shebao']

    def parse(self, response):
        # 分组
        movie_li_tag_list = response.xpath('//ul[@id="contents"]//li')

        for li_tag in movie_li_tag_list:
            movie_info = TryscrapyspiderItem()
            movie_info["movie_name"] = li_tag.xpath('./h5/a/text()').extract_first()
            movie_info["movie_actor"] = list(
                li_tag.xpath('.//p[@class = "actor"]').extract_first().split('</em>')[1].replace("</p>", "").split(" "))
            movie_info["movie_info_url"] = pre_url + li_tag.xpath("./a/@href").extract_first()
            movie_info["movie_jpg"] = li_tag.xpath("./a/img/@src").extract_first()
            # yield movie_info
            yield scrapy.Request(
                movie_info["movie_info_url"],
                callback=self.parse_movie_info_page,
                # 使用deepcopy 防止不同线程中数据错乱 movie_info 是[] 可以这样用
                # 如果多条信息共用一个item时，item又是[]时，要deepcopy
                meta={"item": movie_info}
            )
        # 下一页url
        next_page_url = response.xpath('//a[@class="next pagegbk"]/@href').extract_first()
        last_page_url = response.xpath('//div[@class="pages long-page"]/a[last()-1]/@href').extract_first()
        if next_page_url != last_page_url:
            next_page_url = pre_url + next_page_url
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )
        pass

    def parse_movie_info_page(self, response):
        movie_info = response.meta["item"]
        movie_info["add_time"] = response.xpath(
            '//div[@class="info fn-clear"]//span[@id="addtime"]/text()').extract_first()
        download_str = response.xpath('//div[@class="con4"]/script[3]/text()').extract_first()
        movie_info["thunder"] = download_str.split('"')[1].split('###')[0]
        movie_info["http_download_url"] = download_str.split('###')[1]
        # var GvodUrls = unescape("magnet:?xt=urn:btih:C6BB94758ADDF4CFA2E4D84A3F5EA2B5EBD47A7E&dn=###http://down.aqdya.net/vod/a/miaaadd214.rmvb###");
        yield movie_info
