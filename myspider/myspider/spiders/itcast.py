# -*- coding: utf-8 -*-
import scrapy
import re
import sys
sys.path.append("/Users/mahongying/Desktop/crawler/")
from myspider.items import MyspiderItem
import json
import requests
from myspider.settings import USER_AGENT
class ItcastSpider(scrapy.Spider):
    name = 'itcast'#爬虫名字
    #allowed_domains = ['https://ieeexplore.ieee.org']#爬取的范围
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }

    start_urls = ["https://dblp.uni-trier.de/db/journals/?pos="+str(i+1) for i in range(0,4517,100)]#开始的URL

    def parse(self, response):
        #处理start_url对应的响应
        res1 = response.xpath("//div[@id='browse-journals-output']//div[@class='hide-body']//a")
        item = MyspiderItem()
        for url in res1:
            name = url.xpath("./text()").extract_first()
            tempurl = url.xpath(".//@href").extract()[0]
            if re.match('IEEE',name,re.IGNORECASE):
                item["journal"] = name
                yield  scrapy.Request(
                    url=tempurl,
                    callback=self.parse_joural_url,
                    meta={"item":item}

                 )
    def parse_joural_url(self,response):
        item  = response.meta['item']
        url_list = response.xpath("//div[@id='main']/ul")
        for url in url_list:
            url =url.xpath(".//li/a/@href").extract_first()
            yield scrapy.Request(
                url = url,
                callback=self.parse_json_html,
                meta = {"item":item}
            )

    def parse_json_html(self,response):
        item = response.meta['item']
        json_file = response.xpath("//div[@id='main']/header[1]/nav/ul/li[1]/div[1]/a/@href").extract_first()
        yield scrapy.Request(
            url = json_file[:-3] + "json",
            callback=self.parse_json_html_content,
            meta = {"item":item}
        )
    def parse_json_html_content(self,response):
        item = response.meta['item']
        js = json.loads(response.body)
        js = js['result']['hits']['hit']
        # import random,os
        # if not os.path.exists('./test/'):
        #     os.mkdir('./test/')
        # with open("./test/"+str(random.random())+".json",'w') as f:
        #     json.dump(js,f)
        #     f.close()
        base_url = 'https://ieeexplore.ieee.org/rest/document/'
        for each_item in js:
            item["authors"] = each_item['info']['authors']['author']
            item['title'] = each_item['info']['title']
            item['venue'] = each_item['info']['venue']
            item['year'] = each_item['info']['year']
            item['url']=each_item['info']['ee']
            #r = requests.get(url = each_item['info']['ee'],headers =USER_AGENT,timeout = 30,allow_redirects=False)
            #item['url'] = r.headers['location']
            #print(item)
            yield item








if  __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl itcast".split())