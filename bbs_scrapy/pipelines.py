# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class FidPipeline(object):
    def process_item(self, item, spider):
        print spider
        subject=item['subject']
        if subject.find('forum-464703-thread')>0:
            pass
        else:
            return item

class SavePipeLine(object):
    def process_item(self,item,spide):
        print item['url']
        print item['subject']
        return item