import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow, QTableWidgetItem, QInputDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from UI_To_Py.Login_Window import Ui_Dialog as LoginUI
from UI_To_Py.Register_Window import Ui_Dialog as RegisterUI
from UI_To_Py.MainWindow import Ui_MainWindow as MainUI
from UI_To_Py.AddBook import Ui_Dialog as AddBookUI
from UI_To_Py.SearchWindow import Ui_Dialog as SearchUI
from UI_To_Py.UpdateBookWindow import Ui_Dialog as UpdateBookUI
from db.database import db
from styles.animations import animation_manager
from styles.clean_modern_styles import *

class LoginWindow(QDialog, LoginUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(LOGIN_STYLE)  # 应用现代化样式
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
        # 添加窗口切换动画
        animation_manager.fade_out(self, 200)
        QTimer.singleShot(200, lambda: (
            self.register_window.show(),
            animation_manager.slide_in_from_right(self.register_window, 400),
            self.close()
        ))

class RegisterWindow(QDialog, RegisterUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(REGISTER_STYLE)  # 应用现代化样式
        self.setup_connections()
        # 添加淡入动画
        QTimer.singleShot(100, lambda: animation_manager.fade_in(self))
        
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
        # 添加窗口切换动画
        animation_manager.fade_out(self, 200)
        QTimer.singleShot(200, lambda: (
            self.login_window.show(),
            animation_manager.slide_in_from_left(self.login_window, 400),
            self.close()
        ))

class AddBookDialog(QDialog, AddBookUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(ADD_BOOK_STYLE)  # 应用现代化样式
        self.setup_connections()
        # 添加弹跳动画
        QTimer.singleShot(100, lambda: animation_manager.bounce_in(self))
        
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

class SearchWindow(QDialog, SearchUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(SEARCH_WINDOW_STYLE)  # 应用现代化样式
        self.setup_connections()
        # 添加淡入动画
        QTimer.singleShot(100, lambda: animation_manager.fade_in(self))
        
    def setup_connections(self):
        """连接信号和槽"""
        self.searchButton.clicked.connect(self.search_books)
        self.clearButton.clicked.connect(self.clear_results)
        self.closeButton.clicked.connect(self.close)
        # 支持回车键搜索
        self.searchLineEdit.returnPressed.connect(self.search_books)
        
    def search_books(self):
        """搜索图书功能"""
        keyword = self.searchLineEdit.text().strip()
        if not keyword:
            QMessageBox.warning(self, "警告", "请输入搜索关键词")
            return
            
        # 调用数据库搜索方法
        books = db.search_books(keyword)
        
        if not books:
            self.resultTextEdit.setText("未找到匹配的图书。")
            return
            
        # 格式化搜索结果
        result_text = f"找到 {len(books)} 本相关图书：\n\n"
        
        for i, book in enumerate(books, 1):
            # book数据结构: (id, title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes)
            result_text += f"【{i}】\n"
            result_text += f"书名: {book[1]}\n"
            result_text += f"作者: {book[2] or '未知'}\n"
            result_text += f"存放位置: {book[3] or '未指定'}\n"
            result_text += f"原价: ¥{book[4]}\n"
            result_text += f"出版年份: {book[5]}\n"
            result_text += f"出版社: {book[6] or '未知'}\n"
            result_text += f"数量: {book[7]}\n"
            result_text += f"购买日期: {book[8]}\n"
            result_text += f"购买价格: ¥{book[9]}\n"
            if book[10]:  # 备注
                result_text += f"备注: {book[10]}\n"
            result_text += "-" * 30 + "\n\n"
            
        self.resultTextEdit.setText(result_text)
        
    def clear_results(self):
        """清空搜索结果"""
        self.searchLineEdit.clear()
        self.resultTextEdit.clear()

class UpdateBookWindow(QDialog, UpdateBookUI):
    def __init__(self, book_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(UPDATE_BOOK_STYLE)  # 应用现代化样式
        self.book_id = book_id
        self.setup_connections()
        self.load_book_data()
        # 添加淡入动画
        QTimer.singleShot(100, lambda: animation_manager.fade_in(self))
        
    def setup_connections(self):
        """连接信号和槽"""
        self.confirmButton.clicked.connect(self.confirm_update)
        self.cancelButton.clicked.connect(self.reject)
        
    def load_book_data(self):
        """加载图书数据到表单"""
        # 从数据库获取图书信息
        books = db.get_all_books()
        book_data = None
        
        for book in books:
            if book[0] == self.book_id:  # book[0] 是 ID
                book_data = book
                break
                
        if not book_data:
            QMessageBox.warning(self, "错误", "未找到指定的图书")
            self.reject()
            return
            
        # 填充表单数据
        # book数据结构: (id, title, author, location, original_price, publication_year, publisher, quantity, purchase_date, purchase_price, notes)
        self.bookTitleEdit.setText(book_data[1] or "")
        self.authorEdit.setText(book_data[2] or "")
        self.locationEdit.setText(book_data[3] or "")
        self.originalPriceSpinBox.setValue(float(book_data[4]) if book_data[4] else 0.0)
        self.publicationYearSpinBox.setValue(int(book_data[5]) if book_data[5] else 2024)
        self.publisherEdit.setText(book_data[6] or "")
        self.quantitySpinBox.setValue(int(book_data[7]) if book_data[7] else 1)
        
        # 处理购买日期
        if book_data[8]:
            from PyQt6.QtCore import QDate
            try:
                date_parts = book_data[8].split('-')
                if len(date_parts) == 3:
                    year, month, day = map(int, date_parts)
                    self.purchaseDateEdit.setDate(QDate(year, month, day))
            except:
                pass  # 如果日期格式有问题，使用默认值
                
        self.purchasePriceSpinBox.setValue(float(book_data[9]) if book_data[9] else 0.0)
        self.notesEdit.setPlainText(book_data[10] or "")
        
    def confirm_update(self):
        """确认更新图书信息"""
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
        
        # 调用数据库更新方法
        success, message = db.update_book(
            self.book_id, title, author, location, original_price, 
            publication_year, publisher, quantity, purchase_date, 
            purchase_price, notes
        )
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.accept()  # 关闭对话框并返回成功
        else:
            QMessageBox.warning(self, "失败", message)

class MainWindow(QMainWindow, MainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(MAIN_WINDOW_STYLE)  # 应用现代化样式
        # 强制设置按钮样式，确保可见性
        self.set_button_styles()
        self.setup_connections()
        self.load_books_data()
        
    def set_button_styles(self):
        """强制设置按钮样式，确保可见性"""
        # 添加图书按钮 - 绿色
        self.addButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #52c41a, stop:1 #389e0d);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 140px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #73d13d, stop:1 #52c41a);
            }
        """)
        
        # 查询图书按钮 - 蓝绿色
        self.searchButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #00b894, stop:1 #00a085);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 140px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #00cec9, stop:1 #00b894);
            }
        """)
        
        # 删除图书按钮 - 红色
        self.deleteButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ff6b6b, stop:1 #ee5a52);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 140px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ff7979, stop:1 #f55a5a);
            }
        """)
        
        # 更新图书按钮 - 橙色
        self.updateButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #fdcb6e, stop:1 #e17055);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 140px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ffeaa7, stop:1 #fab1a0);
            }
        """)
        
        # 退出系统按钮 - 灰色
        self.exitButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #636e72, stop:1 #2d3436);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 140px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #74b9ff, stop:1 #0984e3);
            }
        """)
        
    def setup_connections(self):
        self.addButton.clicked.connect(self.add_book)
        self.deleteButton.clicked.connect(self.delete_book)
        self.searchButton.clicked.connect(self.search_books)
        self.updateButton.clicked.connect(self.update_book)
        self.exitButton.clicked.connect(self.close)
        
        # 为按钮添加悬停动画效果
        self.setup_button_hover_effects()
        
    def setup_button_hover_effects(self):
        """设置按钮悬停效果"""
        # 简化动画，去掉有问题的浮动效果
        pass
        
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
        selection_model = self.bookTable.selectionModel()
        if selection_model is None:
            QMessageBox.warning(self, "警告", "表格选择模型未初始化")
            return
            
        selected_rows = selection_model.selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要删除的图书")
            return
            
        # 获取选中行的书名
        row = selected_rows[0].row()
        first_item = self.bookTable.item(row, 0)  # 第一列是书名
        if first_item is None:
            QMessageBox.warning(self, "警告", "无法获取图书信息")
            return
        book_title = first_item.text()
        
        # 显示确认对话框
        reply = QMessageBox.question(
            self, 
            "确认删除", 
            f"您确定要删除图书《{book_title}》吗？\n\n此操作无法撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # 默认选择"否"
        )
        
        # 如果用户选择"是"，则执行删除
        if reply == QMessageBox.StandardButton.Yes:
            # 获取选中行的ID（从第一列的用户数据中获取）
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
        """打开搜索窗口"""
        search_window = SearchWindow(self)
        search_window.exec()
                    
    def update_book(self):
        """更新图书信息"""
        selection_model = self.bookTable.selectionModel()
        if selection_model is None:
            QMessageBox.warning(self, "警告", "表格选择模型未初始化")
            return
            
        selected_rows = selection_model.selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要更新的图书")
            return
            
        # 获取选中行的ID（从第一列的用户数据中获取）
        row = selected_rows[0].row()
        first_item = self.bookTable.item(row, 0)  # 第一列（书名列）
        if first_item:
            book_id = first_item.data(Qt.ItemDataRole.UserRole)
            # 打开更新窗口
            update_window = UpdateBookWindow(book_id, self)
            if update_window.exec() == QDialog.DialogCode.Accepted:
                self.load_books_data()  # 重新加载数据
        else:
            QMessageBox.warning(self, "失败", "无法获取图书ID")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())