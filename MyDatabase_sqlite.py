import sqlite3

class DB:
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except:
            pass

    def execute(self, sql, params=()):
        return self.cursor.execute(sql, params)

    def fetchall(self, sql, params=()):
        cur = self.cursor.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def fetchone(self, sql, params=()):
        cur = self.cursor.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None
