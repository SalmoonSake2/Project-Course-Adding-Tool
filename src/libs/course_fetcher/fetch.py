'''
fetch.py

author:

Azusa Kaze
Salmoon Sake
-------------------------------------------------------------------------------

從網路上擷取陽明的課表資料
'''

import os
import re
from typing import Literal, Union, get_args # type annotation

import pandas as pd # 資料處理用
import requests # 資料獲取用

class fetcher:
    """
    課程擷取器
    """

    #參數，加上annotation
    FetchTimeType = Literal['y', 'z', '1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd']
    FetchDateType = Literal['M', 'T', 'W', 'R', 'F', 'S', 'U']
    Fetchcostype_dic = {'OCW': '28', '遠距課程': '4', '服務學習': '7', '智財權課程': '8', '性平相關課程': '9', '英文授課': '13', '通識校基本素養': '15', '通識跨院 基本素養': '16', '通識核心課程': '17', '一般實習': '26', '語言領域-中文(含寫作)': '29', '語言領域-英文': '30', '核心通識-哲學與心靈': '31', '核心通識-歷史與文明': '32', '核心通識-社會與經濟': '33', '核心通識-倫理與道德思考': '34', '核心通識-科技與社會': '35', '核心通識-藝術與文化': '36', '博雅選修通識': '37', '基本素養-批判思考': '44', '基本素養-量性推理': '45', '基本素養-組織管理': '46', '基本素養-生命及品格教育': '47', '領域課程-人文與美學': '48', '領域課程-個人、社會與文化': '49', '領域課程-公民與倫理思考': '50', '領域課程-社會中的科技與自然': '51', '語言與溝通-英文': '52', '語言與溝通-國家語言': '53', '語言與溝通-第二外語': '54', '語言與溝通-溝通表達': '55', '語言與溝通-寫作課程': '56', '跨校區課程': '57', '程式相關': '58', '實驗課程': '59', '臨床實習': '60', '大型展演': '61', '專題演講': '62', '書報專題討論': '63', '大學專 題': '64', '大學導師': '65', '臨床導師': '66', '音樂指導(個別指導費)': '67', '音樂分組': '68', '寫作課程': '69', '校際合開課程': '70', '開放隨班附讀': '71', '不支援核心': '73', '社會參與': '74', '媒體資訊判讀': '75', '基礎服務學習': '76', '專業服務學習': '77', '人文關懷': '78', '人權教育': '79', '品德教育': '80', '生命教育': '81'}
    
    def __init__(self):
        # 預設headers
        self.headers = {'user-agent': 'Mozilla/5.0'}

    def __combine_time(self, time_l: list[str] | str | None = None, date_l: list[str] | str | None = None) -> list[str]:
        """
        資料範圍設定

        :param time_l: 時間範圍
        :param date_l: 星期範圍
        :return: 合併資料
        :rtype: list[str]
        """

        # 輸入初處理
        if time_l is None:
            time_l = list(get_args(fetcher.FetchTimeType))
        elif not isinstance(time_l, (list, str)):
            raise TypeError("'time_l' must be a 'list' or 'str'.")
        if date_l is None:
            date_l = list(get_args(fetcher.FetchDateType))
        elif not isinstance(date_l, (list, str)):
            raise TypeError("'date_l' must be a 'list' or 'str'.")
        
        # 日期和時間合併，並存成list
        ret_l = []
        for d in date_l:
            for t in time_l:
                ret_l.append(d + t)
        return ret_l

    def __time_setter(self, string):
        ret_str = ""
        temp = ""
        for j in string:
            if j in list(get_args(fetcher.FetchDateType)):
                temp = j
            else:
                ret_str += temp + j
        return ret_str

    def __time_slicer(self, data: str):
        pattern = r"([A-Za-z0-9]+)|-([A-Z0-9]+)|\[([A-Z]+)\]"
        l = data.split(",")
        base = {"time": [], "class": [], "campus": []}
        for string in l:
            matches = re.findall(pattern, string)
            for m in matches:
                if m[0]:
                    base["time"].append(self.__time_setter(m[0]))
                if m[1]: base["class"].append(m[1])
                if m[2]: base["campus"].append(m[2])
        ret_str = "|".join(base['time']) + "," + "|".join(base["class"]) + "," + "|".join(base["campus"])
        return ret_str

    def fetch_by_date(self,
              progress_var: list[int],
              time_l: Union['fetcher.FetchTimeType', list[str], None] = None,
              date_l: Union['fetcher.FetchDateType', list[str], None] = None,
              acyend: int = 113,
              semend: int = 1,
              full_file_name: str = 'timetableDate.xlsx') -> pd.DataFrame:
        """
        擷取實作: 依時間獲取

        :param time_l: 時間範圍
        :param date_l: 星期範圍
        :param full_file_name: 輸出資料檔名
        :return: :class:`pandas <DataFrame>` object
        :rtype: pandas.DataFrame
        """
        
        # 參數設定
        url = "https://timetable.nycu.edu.tw"
        params = {
        "r": "main/get_cos_list"
        }

        # 獲取資料範圍
        combine_l = self.__combine_time(time_l, date_l)

        # 獲取資料範圍處理
        slic = 7
        run_l = [combine_l[i:i+slic] for i in range(0, len(combine_l), slic)]
        
        # 獲取資料處理
        df_all = pd.DataFrame()
        lenth = len(run_l)
        for i in range(lenth):
            m_crstimes = run_l[i]

            progress_var[0] = int((i/lenth)*100)
            
            # 獲取資料參數
            m_crstime = ",".join(str(i) for i in m_crstimes)
            payload = {"m_acy": acyend,
            "m_sem": semend,
            "m_acyend": acyend,
            "m_semend": semend,
            "m_dep_uid": "**",
            "m_group": "**",
            "m_grade": "**",
            "m_class": "**",
            "m_option": "crstime",
            "m_crsname": "**",
            "m_teaname": "**",
            "m_cos_id": "**",
            "m_cos_code": "**",
            "m_crstime": m_crstime,
            "m_crsoutline": "**",
            "m_costype": "**",
            "m_selcampus": "**"}

            # 獲取資料，並設成dict
            res = requests.post(url,params=params, data=payload,headers=self.headers)
            js = res.json()

            # 資料分層處理(嵌套)
            dic_data = {}
            for key in js:
                sub_js = js[key]["1"]
                costype_keys = list(js[key]["costype"].keys())
                for cos_key in costype_keys:
                    inner_coctype_keys = js[key]["costype"][cos_key]
                    cos_val = [in_key.split("_")[0] for in_key in inner_coctype_keys.keys()]
                    sub_js[cos_key]["brief"] = ",".join(cos_val)

                dic_data = dic_data | sub_js
            
            # dict to DataFrame
            df_raw = pd.DataFrame(dic_data)
            df = df_raw.T
            df_all = pd.concat([df_all, df]) # 併入資料

        # 併入資料格式處理，重設index、去除重複資料
        df_all.reset_index(inplace=True)
        df_all.drop_duplicates(['index'], inplace=True, ignore_index=False)
        df_all["cos_data"] = df_all["cos_time"].apply(self.__time_slicer)

        # 偵測檔名是否支援
        typ = full_file_name.split('.')[-1]
        match typ:
            case 'xlsx':
                df_all.to_excel(full_file_name)
            case _ as e:
                raise ValueError(f"'{e}' is not a valid type")
        return df_all

def check_timetable_update(progress_var:int,
                           progressbar_obj,
                           df:list) -> None:
    '''
    檢查課表是否需要更新
    '''

    if not os.path.exists('timetableDate.xlsx'):

        acy = get_acysem("user_data")[0]
        sem = get_acysem("user_data")[1]

        fetcher().fetch_by_date(progress_var=progress_var,acyend=acy,semend=sem)

    progressbar_obj.pack_forget()

    df[0] = pd.read_excel("timetableDate.xlsx")

def get_data_from_index(df,index:str) -> pd.Series:
    '''
    從永久課號獲取課程相關資訊
    '''
    index_series:pd.Series = df['index']
    n_index = index_series.index[index_series.str.contains(index)][0]
    return df.T[n_index]

def get_acysem(path:str) -> tuple:
    '''
    獲取學年
    '''
    with open(file=path,mode="r",encoding="utf-8") as file:
        for line in file:
            acy = line.split(",")[0]
            sem = line.split(",")[1]
            lang = line.split(",")[2]

    return (acy,sem,lang)