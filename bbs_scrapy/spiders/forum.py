from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from bbs_scrapy.items import DocItem
from scrapy import log
class ForumSpider(BaseSpider):

    def __init__(self, fid=26, *args, **kwargs):
        super(ForumSpider, self).__init__(*args, **kwargs)
        self.fid=fid
        self.start_urls=[]
        for p in range(1,10):
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

        return items

