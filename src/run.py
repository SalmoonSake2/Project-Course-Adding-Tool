'''
run.py

author:

Azusa Kaze
Salmoon Sake
-------------------------------------------------------------------------------

程序的入口，請從這邊開始執行。
'''
import os
import sys

sys.path.append("../")
os.chdir(os.path.abspath(os.path.join(__file__, "../..")))

#檢驗套件是否正確下載
try:
    import ttkbootstrap

except:
    input("缺少必要的套件：ttkbootstrap，請在命令提示字元輸入：pip install ttkbootstrap")
    sys.exit()

try:
    import pandas
except:
    input("缺少必要的套件：pandas，請於命令提示字元輸入：pip install pandas")
    sys.exit()

try:
    import requests
except:
    input("缺少必要的套件：requests，請於命令提示字元輸入：pip install requests")
    sys.exit()

try:
    import openpyxl
except:
    input("缺少必要的套件：openpyxl，請於命令提示字元輸入：pip install openpyxl")
    sys.exit()

from libs.interface.app import APP

APP()