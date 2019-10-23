#!/usr/bin/env python3
# -- coding=utf-8 --
import psycopg2


class PostgreSql(object):
    def __init__(self, db_config):
        super(PostgreSql, self).__init__()
        self.db_config = db_config
        self.conn = psycopg2.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["passwd"],
            database=db_config["database"],
        )
        self.cur = self.conn.cursor()

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
        "database": "test"
    }
    psql = PostgreSql(db_config)
    sql = "SELECT * FROM COMPANY"
    print(psql.select(sql))
