# 🚀 PyQt6 + PyQt6-tools 安装与配置指南

## 📦 下载 PyQt6 和 PyQt6-tools

### 1️⃣ 创建虚拟环境
你可以使用 **conda** 或 **.venv** 创建环境：

```
bash
conda create -n pyqt6_env python=3.10
conda activate pyqt6_env
或
bash
uv init
uv venv
.\.venv\Scripts\activate  
```
2️⃣ 安装依赖包
```
bash
复制代码
pip install pyqt6 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pyqt6-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
✅ -i 之后是镜像源（这里用的是清华源，下载更快）。

#或者uv
uv pip install pyqt6
uv pip install pyqt6-tools
#可选add（配置uv锁）,但可能会出问题
```
3️⃣ 验证安装
```
bash
from PyQt6.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)
label = QLabel('✅ PyQt6 安装成功！')
label.show()
sys.exit(app.exec())
```
运行后，如果能弹出一个窗口并显示“✅ PyQt6 安装成功！”，说明安装成功 🎉。


## 🛠️ VS Code 配置 Qt Designer 和 pyuic6
### ❓ 什么是 Designer 和 pyuic？
  Qt Designer 👉 就像 画图工具，帮你画出漂亮的界面。

  pyuic6 👉 就像 翻译机，把 `.ui`文件翻译成 `Python` 代码。

### ⚙️ 配置步骤
打开 VS Code，安装插件 👉 PYQT Integration，打开插件的设置，找到下面截图示例两个我填入路径（带有蓝色引用的位置）  
找到`pyuic6.exe`和`designer.exe`两个文件的位置  
如果用的是`annconda`,那么得麻烦一点，得去你的`conda`环境下查找。如果用的是`.venv`，那么就在你的项目文件夹下的环境中。

`pyuic6.exe` 在虚拟环境的 `Scripts` 文件夹下。
例如：
   ```
  D:\Anaconda1\envs\pyqt_env\Scripts
  ```
这个 `designer.exe` 的路径
例如：
  ```
  Anaconda1\envs\pyqt_env\Lib\site-packages\qt6_applications\Qt\bin
  ```
你也可以把 `designer.exe` 加入 环境变量，这样就能直接在终端输入：

bash
```
designer
```
就能启动 Qt Designer。

📸 截图示例
<img width="1915" height="1079" alt="屏幕截图 2025-09-10 191645" src="https://github.com/user-attachments/assets/3159606d-7852-46f1-a969-42c3587aee27" />


### 🎯 配置总结
🟢 PyQt6 提供核心功能

🟢 pyqt6-tools 提供 Designer 和 pyuic6


# 创建登录注册功能界面
## 推荐项目结构
```
db
 |--database.py #用来封装数据库操作
ui_file
 |_Login_Window.py
 |_Register_Window.py #存放各个界面
ui_to_py
 |_***.py #存放转换好的py文件
main.py #主文件
```
## 使用 `designer` 创建登录界面和注册界面
<img width="1919" height="1074" alt="屏幕截图 2025-09-23 183003" src="https://github.com/user-attachments/assets/463715de-5731-42bd-886b-0b8b6977dee5" />
<img width="1907" height="1079" alt="屏幕截图 2025-09-23 183126" src="https://github.com/user-attachments/assets/ed271604-2663-4266-941d-a5af556d4479" />


文件--保存--项目新建一个存放`ui_files`的文件夹

## 将 `.ui` -->  `.py`
这里注意给的是文件的你存放ui文件的路径和希望保存转换好py的文件位置,最好再建一个文件夹 `ui_to_py`
```
bash
    pyuic6 mainwindow.ui -o mainwindow.py
```
## 封装数据库类 ，创建 `database.py`配置用户数据库操作
```
import sqlite3
import hashlib
import os
from typing import Optional, Tuple

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
```
## 编写主文件 main.py
```
import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from base_screen import Ui_Dialog
from database import Database
from UI_To_Py.Login_Window import Ui_Dialog as LoginUI
from UI_To_Py.Register_Window import Ui_Dialog as RegisterUI
from db.database import db


class LoginWindow(QDialog, Ui_Dialog):
class LoginWindow(QDialog, LoginUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = Database()

        # 绑定按钮事件
        self.login_pushButton.setText("登录")
        self.sign_pushButton_2.setText("注册")
        self.login_pushButton.clicked.connect(self.login)
        self.sign_pushButton_2.clicked.connect(self.register)

        self.setup_connections()
        
    def setup_connections(self):
        self.Initial_Login_Botton.clicked.connect(self.login)
        self.Initial_Register_Botton.clicked.connect(self.open_register_window)
        
    def login(self):
        username = self.name_line.text()
        password = self.password_line.text()

        if self.db.check_login(username, password):
            QMessageBox.information(self, "成功", "登录成功！")
        username = self.Initial_name_input.text()
        password = self.Initial_password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "警告", "请输入用户名和密码")
            return
            
        success, message = db.authenticate_user(username, password)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", "用户名或密码错误！")
            QMessageBox.warning(self, "失败", message)
            
    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

class RegisterWindow(QDialog, RegisterUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()
        
    def setup_connections(self):
        self.Register_Botton.clicked.connect(self.register)
        self.Register_Return_Botton.clicked.connect(self.return_to_login)
        
    def register(self):
        username = self.name_line.text()
        password = self.password_line.text()

        if self.db.register_user(username, password):
            QMessageBox.information(self, "成功", "注册成功！")
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        confirm_password = self.lineEdit_3.text()
        
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return
            
        success, message = db.register_user(username, password, confirm_password)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", "用户名已存在！")

            QMessageBox.warning(self, "失败", message)
            
    def return_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
```
运行 main.py 测试注册和登录效果





