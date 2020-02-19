# -*- coding: utf-8 -*-
import scrapy
import re
import json


class CangkuspiderSpider(scrapy.Spider):
    '''
    这个是js动态生成的，只用scrapy不太行
    '''
    name = 'cangkuSpider'
    allowed_domains = ['cangku.moe']
    start_urls = ['https://cangku.moe/']

    def start_requests(self):
        with open('cookies_file.json', 'r') as f:
            cookies = json.load(f)
        print(cookies)
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        print(response.body.decode())
        print(re.findall('657116885', response.body.decode()))
        # print(re.findall(r"<from", response.body.decode()))
        # print(response.body)
        # yield scrapy.FormRequest.from_response(
        #     response,
        #     fromdata={"user_login": "657116885@qq.com", "user_password": "657116885", "remember": False},
        #     callback=self.login_callback
        # )
        pass

    def login_callback(self, response):
        print(re.findall('这个人很懒', response.body.decode()))
