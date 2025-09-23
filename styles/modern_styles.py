"""
现代化样式模块
提供带有流动感的现代化UI样式
"""

# 登录窗口样式 - 渐变背景和流动效果
LOGIN_STYLE = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
    border-radius: 10px;
}

QLabel {
    color: white;
    font-size: 16px;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

QLineEdit {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: #333;
    selection-background-color: #667eea;
}

QLineEdit:focus {
    border: 2px solid rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 1.0);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

QLineEdit:hover {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid rgba(255, 255, 255, 0.6);
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff6b6b, stop:1 #ee5a52);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 120px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff7979, stop:1 #f55a5a);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e55656, stop:1 #d63031);
}

QPushButton#Initial_Register_Botton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00b894, stop:1 #00a085);
}

QPushButton#Initial_Register_Botton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00cec9, stop:1 #00b894);
}
"""

# 注册窗口样式
REGISTER_STYLE = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #11998e, stop:1 #38ef7d);
    border-radius: 10px;
}

QLabel {
    color: white;
    font-size: 16px;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

QLineEdit {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: #333;
}

QLineEdit:focus {
    border: 2px solid rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 1.0);
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #6c5ce7, stop:1 #5f3dc4);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 120px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #7d6ef0, stop:1 #6c5ce7);
}

QPushButton#Register_Return_Botton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e84393, stop:1 #d63031);
}
"""

# 主窗口样式
MAIN_WINDOW_STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #f093fb, stop:1 #f5576c);
}

QTableWidget {
    background: rgba(255, 255, 255, 0.95);
    border: none;
    border-radius: 12px;
    gridline-color: rgba(0, 0, 0, 0.1);
    font-size: 14px;
    alternate-background-color: rgba(248, 249, 250, 0.8);
}

QTableWidget::item {
    padding: 12px 8px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

QTableWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(102, 126, 234, 0.3), stop:1 rgba(118, 75, 162, 0.3));
    color: #333;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
    color: white;
    padding: 12px 8px;
    border: none;
    font-weight: bold;
    font-size: 14px;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: bold;
    min-width: 140px;
    min-height: 45px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #7c8bf0, stop:1 #8b5fbf);
    transform: translateY(-1px);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #5a6fd8, stop:1 #6b4c93);
}

QPushButton#deleteButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff6b6b, stop:1 #ee5a52);
}

QPushButton#deleteButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff7979, stop:1 #f55a5a);
}

QPushButton#searchButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00b894, stop:1 #00a085);
}

QPushButton#searchButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00cec9, stop:1 #00b894);
}

QPushButton#updateButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fdcb6e, stop:1 #e17055);
}

QPushButton#updateButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffeaa7, stop:1 #fab1a0);
}

QPushButton#exitButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #636e72, stop:1 #2d3436);
}

QPushButton#exitButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #74b9ff, stop:1 #0984e3);
}
"""

# 添加图书对话框样式
ADD_BOOK_STYLE = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #74b9ff, stop:1 #0984e3);
    border-radius: 15px;
}

QLabel {
    color: white;
    font-size: 16px;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

QScrollArea {
    background: transparent;
    border: none;
}

QWidget#scrollAreaWidgetContents {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
}

QLineEdit, QDoubleSpinBox, QSpinBox, QDateEdit {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(116, 185, 255, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: #333;
    min-height: 20px;
}

QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QDateEdit:focus {
    border: 2px solid #74b9ff;
    background: rgba(255, 255, 255, 1.0);
    box-shadow: 0 0 8px rgba(116, 185, 255, 0.3);
}

QTextEdit {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(116, 185, 255, 0.3);
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #333;
}

QTextEdit:focus {
    border: 2px solid #74b9ff;
    background: rgba(255, 255, 255, 1.0);
}

QPushButton#confirmButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00b894, stop:1 #00a085);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 120px;
}

QPushButton#confirmButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00cec9, stop:1 #00b894);
    transform: translateY(-2px);
}

QPushButton#cancelButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e84393, stop:1 #d63031);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 120px;
}

QPushButton#cancelButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fd79a8, stop:1 #e17055);
    transform: translateY(-2px);
}
"""

# 搜索窗口样式
SEARCH_WINDOW_STYLE = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #a29bfe, stop:1 #6c5ce7);
    border-radius: 15px;
}

QLineEdit {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 16px;
    color: #333;
    min-height: 20px;
}

QLineEdit:focus {
    border: 2px solid rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 1.0);
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

QTextEdit {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 16px;
    font-size: 14px;
    color: #333;
    line-height: 1.6;
}

QPushButton#searchButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00b894, stop:1 #00a085);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 100px;
}

QPushButton#searchButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00cec9, stop:1 #00b894);
    transform: translateY(-2px);
}

QPushButton#clearButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff6b6b, stop:1 #ee5a52);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
}

QPushButton#clearButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff7979, stop:1 #f55a5a);
}

QPushButton#closeButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #636e72, stop:1 #2d3436);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
}
"""

# 更新图书窗口样式
UPDATE_BOOK_STYLE = """
QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #ffecd2, stop:1 #fcb69f);
    border-radius: 15px;
}

QLabel {
    color: #2d3436;
    font-size: 16px;
    font-weight: 500;
}

QLineEdit, QDoubleSpinBox, QSpinBox, QDateEdit {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(252, 182, 159, 0.5);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    color: #333;
    min-height: 20px;
}

QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QDateEdit:focus {
    border: 2px solid #fcb69f;
    background: rgba(255, 255, 255, 1.0);
}

QTextEdit {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(252, 182, 159, 0.5);
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #333;
}

QPushButton#confirmButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fdcb6e, stop:1 #e17055);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 120px;
}

QPushButton#confirmButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffeaa7, stop:1 #fab1a0);
}

QPushButton#cancelButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #74b9ff, stop:1 #0984e3);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    min-width: 120px;
}
"""