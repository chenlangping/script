#!/usr/bin/env python3
# -- coding=utf-8 --
import pymysql


class Mysql(object):
    def __init__(self, db_config):
        super(Mysql, self).__init__()
        self.db_config = db_config
        self.conn = pymysql.connect(
            host=db_config["host"],
            user=db_config["user"],
            passwd=db_config["passwd"],
            db=db_config["db"],
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def show_databases(self):
        self.cur.execute('SHOW DATABASES')
        return [i[0] for i in self.cur.fetchall()]

    def show_tables(self):
        self.cur.execute('SHOW TABLES')
        return [i[0] for i in self.cur.fetchall()]

    def select(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def execute(self, sql):
        return self.cur.execute(sql)

    def __del__(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    db_config = {
        "host": "localhost",
        "user": "root",
        "passwd": "123456",
        "db": "test"
    }
    mysql = Mysql(db_config)
    print(mysql.show_databases())
    print(mysql.show_tables())
    sql = "SELECT * FROM COMPANY"
    print(mysql.select(sql))
