'''
run.py

author:

Azusa Kaze
Salmoon Sake

annoucement:
本軟體除了使用了python原生庫外，
也使用了以下第三方library:

pandas: https://pandas.pydata.org/
用於資料分析、歸整

requests: https://github.com/psf/requests
用於網路爬蟲，進行課表更新

ttkbootstrap: https://github.com/israel-dryer/ttkbootstrap/
用於軟體介面，呈現GUI

已知問題：
- 結果畫面有時無法順利滾動，這是由於scrollframe被物件遮掩所致，滑鼠移一下位置就好了。
- 希望老師能給A+

備註：需要根據requirements 安裝所需的包
-------------------------------------------------------------------------------

程序的入口，請從這邊開始執行。
'''
import os
os.chdir(os.path.dirname(os.path.dirname(__file__)))

from libs.interface.app import APP

APP()