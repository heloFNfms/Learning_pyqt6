import pymysql

class MySQLDB:
    def __init__(self, host="localhost", port=3306,
                 user="root", password="WZY216814wzy",
                 database="testdb", autocommit=False):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor  # 让结果是 dict
        )
        self.cursor = self.conn.cursor()
        self.autocommit = autocommit

    def close(self):
        try:
            if not self.autocommit:
                self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        elif not self.autocommit:
            self.conn.commit()
        self.close()

    def execute(self, sql, params=()):
        """执行 SQL"""
        self.cursor.execute(sql, params)
        if self.autocommit:
            self.conn.commit()
        return self.cursor

    def fetchall(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetchone(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()
