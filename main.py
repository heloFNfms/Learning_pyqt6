import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow, QTableWidgetItem, QInputDialog
from PyQt6.QtCore import Qt
from UI_To_Py.Login_Window import Ui_Dialog as LoginUI
from UI_To_Py.Register_Window import Ui_Dialog as RegisterUI
from UI_To_Py.MainWindow import Ui_MainWindow as MainUI
from UI_To_Py.AddBook import Ui_Dialog as AddBookUI
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

class AddBookDialog(QDialog, AddBookUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_connections()
        
    def setup_connections(self):
        self.confirmButton.clicked.connect(self.confirm_add)
        self.cancelButton.clicked.connect(self.reject)
        
    def confirm_add(self):
        # 验证必填字段
        if not self.bookTitleEdit.text().strip():
            QMessageBox.warning(self, "警告", "请输入书名")
            return
            
        # 获取表单数据
        title = self.bookTitleEdit.text().strip()
        author = self.authorEdit.text().strip() or "未知作者"
        location = self.locationEdit.text().strip() or "未指定"
        original_price = self.originalPriceSpinBox.value()
        publication_year = self.publicationYearSpinBox.value()
        publisher = self.publisherEdit.text().strip() or "未知出版社"
        quantity = self.quantitySpinBox.value()
        purchase_date = self.purchaseDateEdit.date().toString("yyyy-MM-dd")
        purchase_price = self.purchasePriceSpinBox.value()
        notes = self.notesEdit.toPlainText().strip()
        
        # 调用数据库添加方法
        success, message = db.add_book(
            title, author, location, original_price, publication_year,
            publisher, quantity, purchase_date, purchase_price, notes
        )
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept()  # 关闭对话框并返回成功
        else:
            QMessageBox.warning(self, "失败", message)
            
    def get_book_data(self):
        """获取图书数据（用于编辑模式）"""
        return {
            'title': self.bookTitleEdit.text().strip(),
            'author': self.authorEdit.text().strip(),
            'location': self.locationEdit.text().strip(),
            'original_price': self.originalPriceSpinBox.value(),
            'publication_year': self.publicationYearSpinBox.value(),
            'publisher': self.publisherEdit.text().strip(),
            'quantity': self.quantitySpinBox.value(),
            'purchase_date': self.purchaseDateEdit.date().toString("yyyy-MM-dd"),
            'purchase_price': self.purchasePriceSpinBox.value(),
            'notes': self.notesEdit.toPlainText().strip()
        }

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
            # book数据结构: (id, title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes)
            # 表格列: 书名, 作者, 存放位置, 原价, 出版年份, 出版社, 数量, 购买日期, 购买价格, 备注
            
            # 将图书ID存储为行的用户数据，而不是显示在表格中
            book_id = book[0]
            
            # 显示图书信息（跳过ID，从第1个元素开始）
            display_data = book[1:]  # 跳过ID
            for col, data in enumerate(display_data):
                item = QTableWidgetItem(str(data) if data is not None else "")
                # 将图书ID存储在第一列的用户数据中
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, book_id)
                self.bookTable.setItem(row, col, item)
                
    def add_book(self):
        """添加图书功能"""
        dialog = AddBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_books_data()  # 重新加载数据
            
    def delete_book(self):
        """删除选中的图书"""
        selected_rows = self.bookTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要删除的图书")
            return
            
        # 获取选中行的ID（从第一列的用户数据中获取）
        row = selected_rows[0].row()
        first_item = self.bookTable.item(row, 0)  # 第一列（书名列）
        if first_item:
            book_id = first_item.data(Qt.ItemDataRole.UserRole)
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
        # 使用输入对话框获取搜索关键词
        keyword, ok = QInputDialog.getText(self, "搜索", "请输入搜索关键词:")
        if ok and keyword:
            books = db.search_books(keyword)
            self.bookTable.setRowCount(len(books))
            
            for row, book in enumerate(books):
                # book数据结构: (id, title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes)
                book_id = book[0]
                
                # 显示图书信息（跳过ID，从第1个元素开始）
                display_data = book[1:]  # 跳过ID
                for col, data in enumerate(display_data):
                    item = QTableWidgetItem(str(data) if data is not None else "")
                    # 将图书ID存储在第一列的用户数据中
                    if col == 0:
                        item.setData(Qt.ItemDataRole.UserRole, book_id)
                    self.bookTable.setItem(row, col, item)
        elif ok and not keyword:
            # 如果输入为空，显示所有图书
            self.load_books_data()
                    
    def update_book(self):
        """更新图书信息"""
        selected_rows = self.bookTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要更新的图书")
            return
            
        # 获取选中行的ID（从第一列的用户数据中获取）
        row = selected_rows[0].row()
        first_item = self.bookTable.item(row, 0)  # 第一列（书名列）
        if first_item:
            book_id = first_item.data(Qt.ItemDataRole.UserRole)
            # 这里应该打开一个对话框来编辑图书信息
            QMessageBox.information(self, "提示", f"更新功能已触发，图书ID: {book_id}")
        else:
            QMessageBox.warning(self, "失败", "无法获取图书ID")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())