__author__ = 'paul'

from cassandra.cluster import Cluster
from bbs_scrapy.items import BookItem
from datetime import datetime

class ThreadRepo(object):
    def __init__(self):
        self.cluster = Cluster(["139.219.132.197"],protocol_version=3)
        self.session = self.cluster.connect('docs')
        self.prepare_insert = self.session.prepare(
        """
          insert into docs.document(url,author,source,subject,chapters,tags,content,visited,created_at, updated_at,indexed_at) VALUES (
          ?,?,?,?,?,?,?,?,?,?,?
          )
        """)

        self.prepare_update_chapter = self.session.prepare("""
            insert into docs.document(url,chapters) values (?,?)
        """)

        self.prepare_add_fetch_record = self.session.prepare("""
            insert into docs.fetch_list (url, status) values (?,?)
        """)

        self.prepare_get_fetch_record = self.session.prepare("""
            select * from docs.fetch_list where url = ?
        """)

        self.prepare_remove_fetch_record= self.session.prepare("""
            delete from docs.fetch_list where url = ?
        """)

        self.prepare_get_fetch_list = self.session.prepare("""
            select * from docs.fetch_list where status = ? limit ?
        """)

    def getFetchList(self,size=100):
        rows = self.session.execute(self.prepare_get_fetch_list,[0,size])
        for row in rows:
            self.session.execute(self.prepare_add_fetch_record,[row.url,1])
            yield row.url

    def newFetchUrl(self,url):
        results = self.session.execute(self.prepare_get_fetch_record,[url])
        if len(results)<=0:
            self.session.execute(self.prepare_add_fetch_record,[url,0])

    def removeFetchUrl(self,url):
        self.session.execute(self.prepare_remove_fetch_record,[url])

    def updateChapter(self,item):
        self.session.execute(self.prepare_update_chapter,[item['bookUrl'],item['chapters']])

    def insertDocument(self,item):
        self.session.execute(self.prepare_insert,
            [item['url'],
             item['author'],
             item['source'],
             item['subject'],
             item['chapters'],
             item['tags'],
             item['content'],
             item['visited'],
             item['createdAt'],
             item['updatedAt'],
             item['indexedAt']]
        )
        self.removeFetchUrl(item['url'])

    def close(self):
        self.cluster.shutdown()
        self.session.shutdown()

if __name__ == '__main__':
    cluster = Cluster(['139.219.132.197'],protocol_version=3)
    session = cluster.connect('docs')
    print cluster
    rows=session.execute("select url from document;")
    ps = session.prepare("delete chapters['abc'] from document where url=?")
    for row in rows:
        session.execute(ps,[row.url])
    cluster.shutdown()
    session.shutdown()
    print 'test'