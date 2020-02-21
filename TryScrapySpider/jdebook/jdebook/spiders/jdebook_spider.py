# -*- coding: utf-8 -*-
import scrapy
import re
# import json
from pprint import pprint
import demjson
from copy import deepcopy


class JdebookSpiderSpider(scrapy.Spider):
    '''
    因为网页上获取的json数据不是标准的
    用demjson解析
    用json很麻烦
    解决方案https://segmentfault.com/q/1010000006090535
    https://www.jianshu.com/p/6295738168d3
    有很多json库
    具体情况具体使用吧
    '''
    name = 'jdebook_spider'
    allowed_domains = ['e.jd.com', 'list.jd.com', 'item.jd.com', 'gw-e.jd.com']
    start_urls = ['http://e.jd.com/']

    def start_requests(self):
        cookies_str = '__jda=122270672.403497943.1577959838.1577959838.1582190614.1; __jdv=122270672|direct|-|none|-|1582190614382; __jdc=122270672; __jdu=403497943; areaId=11; ipLoc-djd=11-880-881-0; 3AB9D23F7A4B3C9B=XQSOA7OVQLC7DJYX6MYCPUHD4OMDIQOFJNU7F3P27AGQZMTI2QIWDNDVPSPSXCG2LY5MP7VTHVMBS2KNLL37XJFDJE; _gcl_au=1.1.1076745876.1582190778; shshshfp=d8c79ed9e3b4a53032fcc5c9a94b191e; shshshfpa=007bd135-1faf-649e-8bd9-aaef98e9289b-1582190927; shshshfpb=yUC%2B53fnm7p8Ta%2Ffhue2QBg%3D%3D; shshshsID=df9c7cc8ff0e16910b264e0c20985660_2_1582190952276; __jdb=122270672.17.403497943|1.1582190614'
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        book_data_json = re.findall(r"menu:(.*?)submenu:", response.body.decode('gbk').strip(), re.DOTALL)
        book_data_json = "".join(book_data_json).replace("\n", "")
        book_data_json = book_data_json.replace(" ", "")[:-1]
        data = demjson.decode(book_data_json)
        data = data[1:]

        for big_class in data:
            item = {}
            item["b_class_name"] = big_class["NAME"]
            item["b_class_url"] = "https:" + big_class["URL"]
            s_class_list = big_class["children"]
            for s_class in s_class_list:
                item["s_class_name"] = s_class["NAME"]
                item["s_class_url"] = s_class["URL"]
                item["s_class_url"] = "https:" + item["s_class_url"]
                if "products" in item["s_class_url"]:
                    # 需要转换url
                    cat = item["s_class_url"].split('/')[-1].split(".")[0].replace("-", ",")
                    item["s_class_url"] = "https://list.jd.com/list.html?cat=" + cat
                yield scrapy.Request(
                    item["s_class_url"],
                    callback=self.parse_list_page,
                    meta={"item": deepcopy(item)}
                )

    def parse_list_page(self, response):
        item = response.meta["item"]
        # print(item)
        li_list = response.xpath('//li[@class="gl-item"]')
        for li in li_list:
            item["book_name"] = li.xpath('.//div[@class="p-name"]//em/text()').extract_first()
            # item["book_img"] = "http:" + li.xpath('.//div[@class="p-img"]//img/@src').extract_first()
            item["book_img"] = "http:" + li.xpath('//div[@class="p-img"]//img/@src').extract_first()
            # item["book_writer"] = li.xpath('.//div[@class="p-bookdetails"]/span/span/text()').extract_first()
            # 价格是js生成的
            # item["book_price"] = li.xpath('.//div[@class="p-price"]/strong[@class="J_price"]').extract_first()
            item["book_store"] = li.xpath('.//span[@class="p-bi-store"]/a/@title').extract_first()
            item["book_date"] = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()
            item["book_info_url"] = "https:" + li.xpath('.//div[@class="p-name"]/a/@href').extract_first()
            yield scrapy.Request(
                item["book_info_url"],
                callback=self.parse_book_info_page,
                meta={"item": deepcopy(item)}
            )
        # print(item)
        next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
        if next_url is not None:
            next_url = "https://list.jd.com" + next_url
            # print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_list_page,
                meta={"item": item}
            )

    def parse_book_info_page(self, response):
        item = response.meta["item"]
        book_code = re.findall("skuid: (.*?),", response.body.decode('gbk').strip(), re.DOTALL)
        book_code = book_code[0] if len(book_code) > 0 else None
        item["book_author"] = ""
        authors = response.xpath('//div[@class="author"]/a')
        for author in authors:
            item["book_author"] += author.xpath('.//text()').extract_first()
        # 不好去取价格，有很多价格
        # "https://gw-e.jd.com/forBookCode/forBookCode_getEbookInFoAndOrginPrices4JSONP.action?bookCodes=30459269&callback=jQuery8292803&_=1582262462938"
        # item["book_price"] = response.xpath(
        #     '//div[@class="dd"]//span[@class="p-price"]//span[contains(@class,"price")]/text()').extract_first()
        price_url = "https://gw-e.jd.com/forBookCode/forBookCode_getEbookInFoAndOrginPrices4JSONP.action?bookCodes={}".format(
            book_code)

        yield scrapy.Request(
            price_url,
            callback=self.parse_book_price,
            meta={"item": deepcopy(item)}
        )

    def parse_book_price(self, response):
        item = response.meta["item"]
        item["book_price"] = re.findall('"jdPrice":(.*?),', response.body.decode('utf-8'))
        item["book_price"] = item["book_price"][0] if len(item["book_price"]) > 0 else None
        yield item
