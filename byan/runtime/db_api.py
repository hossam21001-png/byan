"""دعم SQLite للغة بيان"""
import sqlite3
import os


class ByanDB:
    def __init__(self, db_path='byan_data.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def execute(self, sql, params=None):
        if not self.conn:
            self.connect()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor

    def fetchall(self, sql, params=None):
        if not self.conn:
            self.connect()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
