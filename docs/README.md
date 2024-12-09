
# 陽明交通大學選課系統改良

## 概述
陽明交通大學選課系統改良版，以python編寫。它提供一個更加方便直觀的選課環境。例如直接從
對應的時段選課，無須頻繁切換課表及選課網頁。

本軟體除了使用了python原生庫外，也使用了以下第三方library:

### pillow: https://pypi.org/project/pillow/
用於圖像處理

### pandas: https://pandas.pydata.org/
用於資料分析、歸整

### requests: https://github.com/psf/requests
用於網路爬蟲，進行課表更新

### ttkbootstrap: https://github.com/israel-dryer/ttkbootstrap/
用於軟體介面，呈現GUI

### openpyxl: https://pypi.org/project/openpyxl/
處理excel

## 安裝
依序於終端Terminal執行以下命令：
```
pip install pillow
pip install ttkbootstrap
pip install pandas
pip install requests
pip install openpyxl
```
或是在終端機執行
```
pip install -r requirements.txt
```

## 執行
以python執行位於src目錄下的run.py檔案即可。

## 已知問題
- 結果畫面有時無法順利滾動，這是由於scrollframe被物件遮掩所致，滑鼠移一下位置就好了。
- 希望老師能給A+
- 大家都是我的好朋友

## 作者
- Azusa Kaze
- Salmoon Sake

## 版本資訊
v1.0 updated in: 2024.12.9
