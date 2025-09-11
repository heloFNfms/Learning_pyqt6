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
