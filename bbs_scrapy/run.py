__author__ = 'paul'
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from bbs_scrapy.spiders.forum import ForumSpider
from bbs_scrapy.spiders.thread import ThreadSpider
from scrapy.utils.project import get_project_settings

spider = ThreadSpider()
settings = get_project_settings()
settings.set('USER_AGENT',"BaiDuSpider")
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()