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

from libs.interface.app import APP

APP()