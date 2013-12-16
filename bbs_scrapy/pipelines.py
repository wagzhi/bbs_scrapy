# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log

class FidPipeline(object):
    def process_item(self, item, spider):
        print spider
        subject=item['url']
        url_filter='forum-%d-thread'%spider.fid
        if subject.find(url_filter)>0:
            return item
        else:
            return None

class SavePipeLine(object):
    def process_item(self,item,spide):
        if item is None:
            return None
        spide.log("%s : %s, %s"%(item['url'],item['subject'],item['read_count']),level=log.INFO)
        return item