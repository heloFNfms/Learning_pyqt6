## 下载pyqt6 和 pyqt6-tools

  ### 1 .先创建一个虚拟环境 conda 或  .venv 都可以

  ### 2 .激活环境后下载：

    pip install pyqt6 -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)【 -i 之后是镜像源】

    pip install pyqt6 tools -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)【tools下载】

    ```Test Text
        from PyQt6.QtWidgets import QApplication, QLabel
        import sys
         
        app = QApplication(sys.argv)
        label = QLabel('PyQt6 安装成功！')
        label.show()
        sys.exit(app.exec())
```


  ### 3 .Vscode 配置 qtdesigner 和 pyuic

    #### 什么是**Designer和pyuic？**

      - **Qt Designer** 就像 **画图工具**，帮你画出漂亮的界面。

      - **pyuic6** 就像 **翻译机**，把 `.ui` 翻译成 Python 代码。

    #### 如何配置（Vscode中）？

      1. 安装插件 -- PYQT Integration

      2. 配置 pyuic6.exe 和 designer.exe 路径 (在环境文件夹下查找），具体在 PYQT Integration 设置中

      3. 可以将 designer.exe 放到环境变量中，下次直接在终端中输入designer就可以启动了
    
      
      ![屏幕截图 2025-09-10 192039](https://github.com/user-attachments/assets/290b41aa-ccba-4f2e-b054-782a1a36f10c)


