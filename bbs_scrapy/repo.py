__author__ = 'paul'

from cassandra.cluster import Cluster
from bbs_scrapy.items import BookItem
from datetime import datetime

class ThreadRepo(object):
    def __init__(self):
        self.cluster = Cluster(["127.0.0.1"],protocol_version=3)
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

        self.prepare_fetch_list = self.session.prepare("""
            insert into docs.fetch_list(url,is_fetched,updated_at) values (?,?,?)
        """)

    def updateFetchList(self,url,isFetched):
        self.session.execute(self.prepare_fetch_list,[url,isFetched,datetime.utcnow()])



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

    def close(self):
        self.cluster.shutdown()
        self.session.shutdown()

if __name__ == '__main__':
    cluster = Cluster(['127.0.0.1'],protocol_version=3)
    session = cluster.connect('docs')
    print cluster
    rows=session.execute("select * from document;")
    print rows[0]
    cluster.shutdown()
    session.shutdown()
    print 'test'