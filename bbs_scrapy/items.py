# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BbsScrapyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()
    desc = Field()

class BookItem(Item):
    subject = Field()
    url = Field()
    content = Field()
    image = Field()
    chapters = Field()
    tags = Field()
    source = Field()
    author = Field()
    visited = Field()
    updatedAt = Field()
    createdAt = Field()
    indexedAt = Field()

class ChapterItem(Item):
    bookUrl = Field()
    chapters = Field()

class DocItem(Item):
    # define the fields for your item here like:
    # name = Field()
    subject = Field()
    fid = Field()
    url = Field()
    read_count = Field()
    reply_count = Field()
