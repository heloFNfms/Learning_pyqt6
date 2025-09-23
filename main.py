import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from UI_To_Py.Login_Window import Ui_Dialog as LoginUI
from UI_To_Py.Register_Window import Ui_Dialog as RegisterUI
from db.database import db

class LoginWindow(QDialog, LoginUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()
        
    def setup_connections(self):
        self.Initial_Login_Botton.clicked.connect(self.login)
        self.Initial_Register_Botton.clicked.connect(self.open_register_window)
        
    def login(self):
        username = self.Initial_name_input.text()
        password = self.Initial_password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "警告", "请输入用户名和密码")
            return
            
        success, message = db.authenticate_user(username, password)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
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
            QMessageBox.warning(self, "失败", message)
            
    def return_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())