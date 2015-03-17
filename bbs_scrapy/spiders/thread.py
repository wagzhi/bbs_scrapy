#coding=utf-8

__author__ = 'paul'

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request.form import FormRequest
from bbs_scrapy.items import BookItem,ChapterItem
from scrapy.http import Request
from scrapy import log
from HTMLParser import HTMLParser
from datetime import datetime,timedelta
import simplejson as json
from bbs_scrapy.repo import ThreadRepo

class ThreadSpider(Spider):

    allowed_domains = ["19lou.com"]
    name = u'thread'
    source = 1
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Cache-Control":"max-age=0",
        #"User-Agent":"BaiDuSpider",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
        "Referer": "http://www.19lou.com/login"
    }


    def __init__(self, url='http://www.19lou.com/forum-464884-thread-10831420794960236-1-1.html', *args, **kwargs):
        '''
            抓取指定fid板块数据
        '''
        super(ThreadSpider, self).__init__(*args, **kwargs)
        self.start_urls.append(url)
        self.threadRepo = ThreadRepo()

    def start_requests1(self):
        return [FormRequest(u"https://www.19lou.com/login",
                            formdata={u'userName': u'dunsword',
                                      u'userPass': u'pass123',
                                      u'refererUrl':u'',
                                      u'checked':u'0',
                                      u'captcha':u'',
                                      u'remember':u'0',
                                      u'ssl':u'on'},
                            callback=self.logged_in)]

    def logged_in(self, response):
    # here you would extract links to follow and return Requests for
    # each of them, with another callback

        cookies = response.headers.getlist('Set-Cookie')
        cs = {"_Z3nY0d4C_":"37XgPK9h-%3D1280-1280-1263-263"}
        for c in cookies:
            kv=c.split(';')[0].split('=')

            cs[kv[0]]=kv[1]
        yield Request(url='http://www.19lou.com/forum-464884-thread-6591413018063694-1-1.html',
                      callback=self.parse,
                      cookies=cs,
                      headers=self.headers)
        #print(response)
    def parse(self,response):
        return self.parse_thread(response)

    def parse_thread(self,response):
        sel=Selector(response)
        item=BookItem()
        item['url']=response.url
        view_head=sel.xpath('//body/div/div[@id="view-hd"]')
        item['subject']=view_head.xpath('h1/a/span/text()').extract()[0]
        item['visited']=int(view_head.xpath('ul/li')[0].xpath('i/text()').extract()[0])
        pages = sel.xpath('//*[@id="view-wrap"]/div[7]/div/a').extract()
        createdAt = sel.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div/div/ul/li')[0].xpath('@title').extract()[0][3:]
        updatedAt =sel.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div/div/ul/li[1]/text()').extract()[0][4:]
        content = sel.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div/div/div/table/tbody/tr/td/div[@class="thread-cont"]')[0].extract()
        hp = ThreadContentHTMLParser()
        hp.feed(content)
        textContent = hp.content
        hp.close()
        item['content']=textContent
        item['createdAt'] = datetime.strptime(createdAt, "%Y-%m-%d %H:%M")
        item['updatedAt'] = datetime.strptime(updatedAt, "%Y-%m-%d %H:%M")
        item['author'] = ""
        item['tags']=[]
        tags = sel.xpath('//*[@id="view-wrap"]/div[8]/div/p/a')
        for tag in tags:
            item['tags'].append(tag.xpath('./span/text()').extract()[0])

        yield  item

        yield FormRequest(u"http://www.19lou.com/post/goodreply/lift",
                    formdata={u'fid': u'464884',
                              u'page': u'1',
                              u'tid':u'10831420794960236'},
                    headers= self.headers,
                    callback=self.parse_chapter)


    def parse_chapter(self,response):
        jsonResult = response.body_as_unicode()
        jsonObj = json.loads(jsonResult)
        self.log(jsonResult,level=log.INFO)
        item =ChapterItem()
        chapters = {}
        for chapter in jsonObj['data']['liftDatas']:
            item =ChapterItem()
            item['bookUrl'] = u"http://www.19lou.com/forum-{fid}-thread-{tid}-1-1.html".format(fid=chapter['fid'],tid=chapter['tid'])
            chapters[chapter['url']]=chapter['subject']
            #item['chapters'][chapter['url']]=chapter['subject']
        item['chapters'] = chapters
        return item


        # def parse_thread_page(self,response):
    #     sel=Selector(response)
    #     item = BookItem()
    #     item['url']=response.url
    #     view_head=sel.xpath('//body/div/div[@id="view-hd"]')
    #     item['subject']=view_head.xpath('h1/a/span/text()').extract()[0]
    #     item['read_count']=view_head.xpath('ul/li')[0].xpath('i/text()').extract()[0]
    #     item['reply_count']=view_head.xpath('ul/li')[1].xpath('i/text()').extract()[0]
    #     item['tags']=[u'ab',u'cd']
    #     # tags = sel.xpath('//*[@id="view-wrap"]/div[8]/div/p/a').extract()
    #     # for tag in tags:
    #     #     item['tags'].append(tag.xpath('./span/text()').extract())
    #     FormRequest(u"http://www.19lou.com/post/goodreply/lift",
    #                 formdata={u'fid': u'464884',
    #                           u'page': u'1',
    #                           u'tid':u'1'},
    #                 callback=self.getChapter).from_response()
    #
    #     return item




# create a subclass and override the handler methods
class ThreadContentHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = u''
    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        pass
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        pass
    def handle_data(self, data):
        self.content += data.strip().strip("/r/n")
