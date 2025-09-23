from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        self.searchLineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLayout.addWidget(self.searchLineEdit)
        self.searchButton = QtWidgets.QPushButton(parent=Dialog)
        self.searchButton.setMinimumSize(QtCore.QSize(80, 30))
        self.searchButton.setObjectName("searchButton")
        self.searchLayout.addWidget(self.searchButton)
        self.verticalLayout_2.addLayout(self.searchLayout)
        self.resultTextEdit = QtWidgets.QTextEdit(parent=Dialog)
        self.resultTextEdit.setReadOnly(True)
        self.resultTextEdit.setObjectName("resultTextEdit")
        self.verticalLayout_2.addWidget(self.resultTextEdit)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.buttonLayout.addItem(spacerItem)
        self.clearButton = QtWidgets.QPushButton(parent=Dialog)
        self.clearButton.setMinimumSize(QtCore.QSize(80, 30))
        self.clearButton.setObjectName("clearButton")
        self.buttonLayout.addWidget(self.clearButton)
        self.closeButton = QtWidgets.QPushButton(parent=Dialog)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.buttonLayout.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.buttonLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "查找书籍"))
        self.searchLineEdit.setPlaceholderText(_translate("Dialog", "请输入书名、作者、出版社等关键词进行搜索"))
        self.searchButton.setText(_translate("Dialog", "查找"))
        self.resultTextEdit.setPlaceholderText(_translate("Dialog", "搜索结果将显示在这里..."))
        self.clearButton.setText(_translate("Dialog", "清空"))
        self.closeButton.setText(_translate("Dialog", "关闭"))
