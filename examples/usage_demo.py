from MyDatabase_sqlite import DB

def main():
    # 持久化数据库：存到本地文件
    db = DB("db/demo.db")  # ":memory:" 会用内存数据库，程序结束数据就没了

    # 建表（如果不存在就创建）
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    # 插入数据（使用 ? 占位 + params，防止 SQL 注入）
    db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 20))
    db.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
    # 更稳妥：重要写操作后手动提交（可选）
    db.conn.commit()

    # 查询多行
    users = db.fetchall("SELECT id, name, age FROM users")
    print(users)  # 例如：[{'id': 1, 'name': 'Alice', 'age': 20}, {'id': 2, 'name': 'Bob', 'age': 25}]

    # 查询一行
    one_user = db.fetchone("SELECT id, name, age FROM users WHERE name = ?", ("Alice",))
    print(one_user)  # 例如：{'id': 1, 'name': 'Alice', 'age': 20}

    # 关闭（会提交未提交的更改并释放资源）
    db.close()

if __name__ == "__main__":
    main()