import sqlite3
import hashlib
import os
from typing import Optional, Tuple, List
from datetime import datetime

class UserDatabase:
    def __init__(self, db_path: str = "users.db"):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径
        """
        # 如果db_path是相对路径，则将其放在db目录下
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path)
        
        self.db_path = os.path.abspath(db_path)
        self.init_database()
    
    def init_database(self):
        """
        初始化数据库表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建图书表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT,
                    location TEXT,
                    original_price REAL,
                    publication_year INTEGER,
                    publisher TEXT,
                    quantity INTEGER DEFAULT 1,
                    purchase_date DATE,
                    purchase_price REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # 检查是否有图书数据，如果没有则添加测试数据
            cursor.execute("SELECT COUNT(*) FROM books")
            count = cursor.fetchone()[0]
            if count == 0:
                self._add_test_data(conn)
    
    def _add_test_data(self, conn):
        """
        添加测试数据
        """
        cursor = conn.cursor()
        test_books = [
            ('高等数学', '同济大学数学组', '3', 36.90, 1999, '同济大学出版社', 3, '2023-9-5', 25.00, '经典数学书'),
            ('大学英语', '外国语组', '1', 72.80, 2005, '清华大学出版社', 1, '2023-9-5', 52.00, '英语教材'),
            ('小王子', '安托万·德·圣埃克苏佩里', '1', 23.6, 2015, '译文出版社', 1, '2020-1-2', 20.00, '经典小说'),
            ('病隙碎笔', '史铁生', '1', 25, 2008, '人民文学出版社', 1, '2021-11-6', 20.00, '对人生的诘问、探索与解答')
        ]
        
        cursor.executemany(
            "INSERT INTO books (title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            test_books
        )
        conn.commit()
    
    def hash_password(self, password: str) -> str:
        """
        对密码进行哈希处理
        :param password: 原始密码
        :return: 哈希后的密码
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def register_user(self, username: str, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        注册新用户
        :param username: 用户名
        :param password: 密码
        :param confirm_password: 确认密码
        :return: (是否成功, 消息)
        """
        # 检查密码确认
        if password != confirm_password:
            return False, "密码和确认密码不匹配"
        
        # 检查用户名是否已存在
        if self.user_exists(username):
            return False, "用户名已存在"
        
        # 检查密码强度（简单检查）
        if len(password) < 6:
            return False, "密码长度至少为6位"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # 插入新用户
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, self.hash_password(password))
                )
                conn.commit()
                return True, "注册成功"
        except sqlite3.Error as e:
            return False, f"数据库错误: {str(e)}"
    
    def user_exists(self, username: str) -> bool:
        """
        检查用户名是否存在
        :param username: 用户名
        :return: 是否存在
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            return cursor.fetchone() is not None
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        验证用户登录
        :param username: 用户名
        :param password: 密码
        :return: (是否成功, 消息)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = ?", 
                (username,)
            )
            result = cursor.fetchone()
            
            if result is None:
                return False, "用户名或密码错误"
            
            stored_hash = result[0]
            if stored_hash == self.hash_password(password):
                return True, "登录成功"
            else:
                return False, "用户名或密码错误"
    
    def get_user_info(self, username: str) -> Optional[Tuple]:
        """
        获取用户信息
        :param username: 用户名
        :return: 用户信息元组或None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, created_at FROM users WHERE username = ?", 
                (username,)
            )
            return cursor.fetchone()
    
    def update_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        更新用户密码
        :param username: 用户名
        :param old_password: 旧密码
        :param new_password: 新密码
        :return: (是否成功, 消息)
        """
        # 验证旧密码
        auth_result, auth_message = self.authenticate_user(username, old_password)
        if not auth_result:
            return False, "旧密码错误"
        
        # 检查新密码强度
        if len(new_password) < 6:
            return False, "新密码长度至少为6位"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE username = ?",
                    (self.hash_password(new_password), username)
                )
                conn.commit()
                return True, "密码更新成功"
        except sqlite3.Error as e:
            return False, f"数据库错误: {str(e)}"

    # 图书管理相关方法
    def add_book(self, title: str, author: str, location: str, original_price: float, 
                 publication_year: int, publisher: str, quantity: int, 
                 purchase_date: str, purchase_price: float, notes: str) -> Tuple[bool, str]:
        """
        添加图书
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes)
                )
                conn.commit()
                return True, "添加成功"
        except sqlite3.Error as e:
            return False, f"数据库错误: {str(e)}"
    
    def get_all_books(self) -> List[Tuple]:
        """
        获取所有图书
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes FROM books")
            return cursor.fetchall()
    
    def search_books(self, keyword: str) -> List[Tuple]:
        """
        搜索图书
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ?",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
            return cursor.fetchall()
    
    def update_book(self, book_id: int, title: str, author: str, location: str, original_price: float, 
                    publication_year: int, publisher: str, quantity: int, 
                    purchase_date: str, purchase_price: float, notes: str) -> Tuple[bool, str]:
        """
        更新图书信息
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE books SET title = ?, author = ?, location = ?, original_price = ?, publication_year = ?, publisher = ?, quantity = ?, purchase_date = ?, purchase_price = ?, notes = ? WHERE id = ?",
                    (title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes, book_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    return False, "未找到该图书"
                return True, "更新成功"
        except sqlite3.Error as e:
            return False, f"数据库错误: {str(e)}"
    
    def delete_book(self, book_id: int) -> Tuple[bool, str]:
        """
        删除图书
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    return False, "未找到该图书"
                return True, "删除成功"
        except sqlite3.Error as e:
            return False, f"数据库错误: {str(e)}"

# 全局数据库实例
db = UserDatabase()

if __name__ == "__main__":
    # 测试代码
    db_instance = UserDatabase()
    
    # 测试注册
    result, message = db_instance.register_user("testuser", "password123", "password123")
    print(f"注册结果: {message}")
    
    # 测试登录
    result, message = db_instance.authenticate_user("testuser", "password123")
    print(f"登录结果: {message}")
    
    # 获取用户信息
    user_info = db_instance.get_user_info("testuser")
    print(f"用户信息: {user_info}")