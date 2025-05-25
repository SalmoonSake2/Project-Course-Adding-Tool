
# 陽明交通大學選課系統改良

## 概述
陽明交通大學選課系統改良版，以python編寫。它提供一個更加方便直觀的選課環境。例如直接從
對應的時段選課，無須頻繁切換課表及選課網頁。

**注意:**
本軟體僅提供模擬選課的介面，不具備真實選課的功能；如需選課請前往學校單一入口登入選課系統。  
本軟體不適用於Anaconda環境，請自行安裝原生python後並依照指示下載必要檔案。  
本軟體僅提供課程資訊，如出現與實際情況不符之情形，後果自行承擔。

## 安裝

下載官方Python:  
https://www.python.org/downloads/  
並依照指示安裝

依序於終端Terminal(或命令提示字元)執行以下命令：
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

- 執行檔案run.py  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case1.png)

- 首次執行需要選擇語言  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case2.png)

- 首次執行需要下載課表至本機(請確認網路狀況後下載)  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case3.png)

- 使用介面  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case4.png)

- 篩選器  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case5.png)

- 點擊時段便能得到符合條件的課程(或使用搜尋按鈕查詢全時段課程)  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case6.png)

- 選課後點擊課程可以看到課程詳細資料  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case7.png)

- 若課堂衝突，會跳出提示  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case8.png)

- 對於有提供課綱連結的課程也能連上  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case9.png)

- 切換課表(須重啟)  
![image](https://github.com/SalmoonSake2/Project---Course-Adding-Tool/blob/main/docs/show_case10.png)

## 備註事項
- 希望老師能給A+
- 大家都是我的好朋友

## 作者
- Azusa Kaze
- Salmoon Sake

## 引用
  
- ttkbootstrap (https://pypi.org/project/ttkbootstrap/)  
  用於使用者介面創建
  
- pandas (https://pypi.org/project/pandas/)  
  用於資料儲存及篩選
  
- requests (https://pypi.org/project/requests/)  
  用於課程資訊擷取
  
- openpyxl (https://pypi.org/project/openpyxl/)  
  用於Excel檔案讀寫

## 版本資訊
v1.3.2 updated in: 2025.05.25

## changinglog (1.3.*)
- 新增了英文模式
- 改善載入速度
- 修復錯誤d0077: 在某些時段的課程會突然閃退
- 修復錯誤d0231: 選擇英文模式後依然有中文時段出現
- 修復錯誤d0232: 切換年份後開啟會閃退
- 修復錯誤d0233: 修正新通識課程配對錯誤問題
- 睡了午覺
