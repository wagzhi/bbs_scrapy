from scrapy.spider import Spider

class BbsSpider(Spider):
    name = "bbs"
    allowed_domains = ["19lou.com"]
    start_urls = [
        "http://www.19lou.com/index.html",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
