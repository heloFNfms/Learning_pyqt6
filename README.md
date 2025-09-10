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








