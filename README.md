# 🚀 PyQt6 + PyQt6-tools 安装与配置指南

## 📦 下载 PyQt6 和 PyQt6-tools

### 1️⃣ 创建虚拟环境
你可以使用 **conda** 或 **.venv** 创建环境：

```
bash
conda create -n pyqt6 python=3.10
conda activate pyqt6
或
bash
python -m venv .venv
.\.venv\Scripts\activate  
```
2️⃣ 安装依赖包
```
bash
复制代码
pip install pyqt6 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pyqt6-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
✅ -i 之后是镜像源（这里用的是清华源，下载更快）。
```
3️⃣ 验证安装
```
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

  pyuic6 👉 就像 翻译机，把 .ui 文件翻译成 Python 代码。

### ⚙️ 配置步骤
打开 VS Code，安装插件 👉 PYQT Integration

在插件设置中，找到 pyuic6.exe 和 designer.exe 的路径（它们在虚拟环境的 Scripts 文件夹下）。

你也可以把 designer.exe 加入 环境变量，这样就能直接在终端输入：

bash
```
designer
```
就能启动 Qt Designer。

📸 截图示例
<img width="1915" height="1079" alt="屏幕截图 2025-09-10 191645" src="https://github.com/user-attachments/assets/3159606d-7852-46f1-a969-42c3587aee27" />


### 🎯 总结
🟢 PyQt6 提供核心功能

🟢 pyqt6-tools 提供 Designer 和 pyuic6

🟢 VS Code 通过插件让开发更丝滑

# 创建一个简单的可视化界面
## 使用 designer 可视化
<img width="1919" height="1079" alt="屏幕截图 2025-09-11 102032" src="https://github.com/user-attachments/assets/e79a5274-1918-4e48-895e-8c743cea47f0" />

文件--保存--项目新建一个存放ui的文件夹

## 将 .ui -->  .py
```
bash
pyuic6 mainwindow.ui -o mainwindow.py
```
## 封装数据库类 ，创建 database.py
```
import sqlite3

class Database:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """如果表不存在，就创建"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password):
        """注册新用户"""
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # 用户名已存在

    def check_login(self, username, password):
        """验证登录"""
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None
```
## 编写主文件 main.py
```
import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from base_screen import Ui_Dialog
from database import Database


class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = Database()

        # 绑定按钮事件
        self.login_pushButton.setText("登录")
        self.sign_pushButton_2.setText("注册")
        self.login_pushButton.clicked.connect(self.login)
        self.sign_pushButton_2.clicked.connect(self.register)

    def login(self):
        username = self.name_line.text()
        password = self.password_line.text()

        if self.db.check_login(username, password):
            QMessageBox.information(self, "成功", "登录成功！")
        else:
            QMessageBox.warning(self, "失败", "用户名或密码错误！")

    def register(self):
        username = self.name_line.text()
        password = self.password_line.text()

        if self.db.register_user(username, password):
            QMessageBox.information(self, "成功", "注册成功！")
        else:
            QMessageBox.warning(self, "失败", "用户名已存在！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
```
运行 main.py 
<img width="1919" height="1079" alt="屏幕截图 2025-09-11 103901" src="https://github.com/user-attachments/assets/3bbb127e-ecf2-41af-b43b-7cdaec9ed591" />




