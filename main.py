import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt6.QtCore import Qt
from UI_To_Py.Login_Window import Ui_Dialog as LoginUI
from UI_To_Py.Register_Window import Ui_Dialog as RegisterUI
from UI_To_Py.MainWindow import Ui_MainWindow as MainUI
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
            # 登录成功后显示主窗口
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
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

class MainWindow(QMainWindow, MainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()
        self.load_books_data()
        
    def setup_connections(self):
        self.addButton.clicked.connect(self.add_book)
        self.deleteButton.clicked.connect(self.delete_book)
        self.searchButton.clicked.connect(self.search_books)
        self.updateButton.clicked.connect(self.update_book)
        self.exitButton.clicked.connect(self.close)
        
    def load_books_data(self):
        """加载所有图书数据到表格"""
        books = db.get_all_books()
        self.bookTable.setRowCount(len(books))
        
        for row, book in enumerate(books):
            # 保存图书ID在第0列（隐藏列）
            id_item = QTableWidgetItem(str(book[0]))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 设置为不可编辑
            self.bookTable.setItem(row, 0, id_item)
            
            # 显示其他图书信息（从第1列开始）
            for col, data in enumerate(book[1:], start=1):
                item = QTableWidgetItem(str(data) if data is not None else "")
                # ID列设置为不可编辑
                if col == 0:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.bookTable.setItem(row, col, item)
                
    def add_book(self):
        """添加图书功能"""
        # 这里可以创建一个对话框来输入图书信息
        # 为简化示例，我们直接添加一本测试图书
        success, message = db.add_book(
            "测试图书", "测试作者", "1", 29.9, 2023, "测试出版社", 1, "2023-10-01", 25.0, "测试备注"
        )
        if success:
            QMessageBox.information(self, "成功", message)
            self.load_books_data()  # 重新加载数据
        else:
            QMessageBox.warning(self, "失败", message)
            
    def delete_book(self):
        """删除选中的图书"""
        selected_rows = self.bookTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要删除的图书")
            return
            
        # 获取选中行的ID
        row = selected_rows[0].row()
        book_id_item = self.bookTable.item(row, 0)  # ID在第0列
        if book_id_item:
            book_id = int(book_id_item.text())
            success, message = db.delete_book(book_id)
            if success:
                QMessageBox.information(self, "成功", message)
                self.load_books_data()  # 重新加载数据
            else:
                QMessageBox.warning(self, "失败", message)
        else:
            QMessageBox.warning(self, "失败", "无法获取图书ID")
            
    def search_books(self):
        """搜索图书"""
        # 这里可以创建一个对话框来输入搜索关键词
        # 为简化示例，我们使用输入对话框获取搜索关键词
        keyword, ok = QMessageBox.getText(self, "搜索", "请输入搜索关键词:")
        if ok and keyword:
            books = db.search_books(keyword)
            self.bookTable.setRowCount(len(books))
            
            for row, book in enumerate(books):
                # 保存图书ID在第0列（隐藏列）
                id_item = QTableWidgetItem(str(book[0]))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.bookTable.setItem(row, 0, id_item)
                
                # 显示其他图书信息（从第1列开始）
                for col, data in enumerate(book[1:], start=1):
                    item = QTableWidgetItem(str(data) if data is not None else "")
                    self.bookTable.setItem(row, col, item)
                    
    def update_book(self):
        """更新图书信息"""
        selected_rows = self.bookTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要更新的图书")
            return
            
        # 获取选中行的ID
        row = selected_rows[0].row()
        book_id_item = self.bookTable.item(row, 0)  # ID在第0列
        if book_id_item:
            # 这里应该打开一个对话框来编辑图书信息
            QMessageBox.information(self, "提示", "更新功能已触发，实际应用中会打开编辑对话框")
        else:
            QMessageBox.warning(self, "失败", "无法获取图书ID")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())