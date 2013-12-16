#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from bbs_scrapy.items import DocItem
from scrapy.http import Request
from scrapy import log
class ForumSpider(BaseSpider):

    def __init__(self, fid=26, *args, **kwargs):
        '''
            抓取指定fid板块数据
        '''
        super(ForumSpider, self).__init__(*args, **kwargs)
        self.fid=fid
        self.start_urls=[]
        for p in range(1,2):
            self.start_urls.append('http://www.19lou.com/forum-%d-%d.html?order=createdat'%(fid,p))

    name = "forum"
    allowed_domains = ["19lou.com"]
    start_urls = (
        #'http://www.19lou.com/forum-26-1.html?order=createdat',
    )

    def parse(self, response):
        self.log(response.url,level=log.INFO)
        sel = Selector(response)
        list_table=sel.xpath('//table[@class="list-data  "]')
        items=[]
        for row in list_table.xpath('//tbody/tr/th/div/a'):
            item=DocItem()
            item['subject']=row.xpath('span/text()').extract()[0]
            item['url']=row.xpath('@href').extract()[0]
            items.append(item)
            yield Request(item['url'], callback=self.parse_thread_page)

        #return items

    def parse_thread_page(self,response):
        sel=Selector(response)
        item=DocItem()
        item['url']=response.url
        view_head=sel.xpath('//body/div/div[@id="view-hd"]')
        item['subject']=view_head.xpath('h1/a/span/text()').extract()[0]
        item['read_count']=view_head.xpath('ul/li')[0].xpath('i/text()').extract()[0]
        item['reply_count']=view_head.xpath('ul/li')[1].xpath('i/text()').extract()[0]
        return item