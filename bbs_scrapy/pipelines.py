#coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from datetime import datetime,timedelta
from bbs_scrapy.items import ChapterItem,BookItem,DocItem
import time

class FidPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,DocItem):
            subject=item['url']
            url_filter='forum-%d-thread'%item['fid']
            if subject.find(url_filter)>0:
                return item
            else:
                return None
        else:
            return item

class FetchListPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,DocItem):
            spider.threadRepo.newFetchUrl(item['url'])
        else:
            return item

class SavePipeLine(object):

    def process_item(self,item,spider):
        if item is None:
            return None

        if isinstance(item,ChapterItem):
            spider.threadRepo.updateChapter(item)
            return item
        elif isinstance(item,BookItem):
            spider.log("%s : %s, %s"%(item['url'],item['subject'],str(item['updatedAt'])),level=log.INFO)
            item['indexedAt'] = datetime.utcnow()
            td = timedelta(seconds=time.timezone)
            item['source']=1
            item['createdAt'] = item['createdAt']+td
            item['updatedAt'] = item['updatedAt']+td
            #spider.log("date: " +str(item['indexedAt']),level=log.INFO)
            #spider.log("tzname: " +str(time.tzname),level=log.INFO)
            spider.threadRepo.insertDocument(item)
            return item
        else:
            return item