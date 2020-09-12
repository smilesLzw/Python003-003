# 学习笔记

- pytesseract
- 数据库连接注意事项

## 如何在 python3 中使用 pytesseract 进行图片识别

[官方文档](https://pypi.org/project/pytesseract/)

### 一：安装 Tesseract-OCR 软件（windows10 安装：）

1. 下载地址：[Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)
2. 安装：Tesseract-OCR 的安装较为简单，一直点击下一步即可
3. 添加到环境变量中

![image](images\clipboard1.png)

![image](images\clipboard2.png)

### 二：安装 python 依赖

```
pip install Pillow
pip install pytesseract
```

### 三：使用

```python
from PIL import Image
import pytesseract

th = Image.open('c_th.jpg')
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

code = pytesseract.image_to_string(th, lang='chi_sim+eng', config=tessdata_dir_config)
print(code)
```

![image](images\clipboard3.png)

## 注意事项

pytesseract 的使用需要安装 Tesseract-OCR，特别在环境变量配置一步尤为重要，很多人代码实现不成功都是因为环境变量的问题。

### 如果出现错误

方法一：重新配置环境变量

方法二：在代码中添加相关变量参数

```
th = Image.open('c_th.jpg')
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

code = pytesseract.image_to_string(th, lang='chi_sim+eng', config=tessdata_dir_config)
print(code)
```

## 数据库连接注意事项

### 1、数据库编码

在进行数据库连接的时候，为了保证编码准确，会先跟数据库管理员进行沟通，然后再进行指定

**需注意，utf-8, utf8， utf8mb4 是有差异的**

utf8mb4 能支持一些表情符号的存储

### 2、事务提交

使用 pymysql 进行数据的插入，修改，删除的时候，当执行完操作后需要进行事物的提交，否则数据库中的数据不会进行更新
