# Scrapy settings for bbs_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bbs_scrapy'

SPIDER_MODULES = ['bbs_scrapy.spiders']
NEWSPIDER_MODULE = 'bbs_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bbs_scrapy (+http://www.yourdomain.com)'
USER_AGENT = 'BaiDuSpider'
DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED=True

ITEM_PIPELINES = {
    #'bbs_scrapy.pipelines.FidPipeline': 300,
    'bbs_scrapy.pipelines.SavePipeLine': 800,
    'bbs_scrapy.pipelines.FidPipeline':600,
    'bbs_scrapy.pipelines.FetchListPipeline':602
}


DOWNLOADER_MIDDLEWARES = {
   # 'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 543,
}