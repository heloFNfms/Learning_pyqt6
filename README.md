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




