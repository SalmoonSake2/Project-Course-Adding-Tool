'''
extract.py

author:

Azusa Kaze
-------------------------------------------------------------------------------

對讀取到的課表一條件進行篩選。
'''

from typing import Literal
import pandas as pd
from libs.interface.ym_mapping import NYCU_CAMPUSES,NYCU_COS_TYPE,NYCU_TIME_SLOTS
from libs.interface.ym_mapping import get_types_from_ezs

condition_lit = Literal['time','campus','class','type','name',"teacher"]
TIME_CONST = NYCU_TIME_SLOTS
CAMPUS_CONST = NYCU_CAMPUSES
TYPE_CONST = NYCU_COS_TYPE

def find(df: pd.DataFrame, condition: condition_lit, condi_args: str| list[str]):
    """擷取資料

    Parameters
    ----------
    df : pd.DataFrame
        總表
    condition : condition_lit
        資料種類
    condi_args : str | list[str]
        資料細項

    Returns
    -------
    pd.DataFrame
    """
    if isinstance(condi_args, str): condi_args = [condi_args]
    match condition:
        case 'time':
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in str(x).split(",")[0] for c_arg in condi_args))]
        case "class":
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in str(x).split(",")[1] for c_arg in condi_args))]
        case 'campus':
            df_temp = df[df['cos_data'].apply(lambda x: any(c_arg in str(x).split(",")[2] for c_arg in condi_args))]
        case "type":
            df_temp = df[df['brief'].apply(lambda x: any(c_arg in str(x) for c_arg in condi_args))]

            #體育不屬於類別資料，需要從dep_id:OU9找出來
            if "體育" in condi_args:
                df_pe = df[df['dep_id'].apply(lambda x: x == "OU9")]
                df_temp = pd.concat([df_temp,df_pe],axis=0,ignore_index=True)
        case "name":
            df_temp = df[df['cos_cname'].apply(lambda x: condi_args[0] in x)]
        case "teacher":
            df_temp = df[df['teacher'].apply(lambda x: condi_args[0] in str(x))]
    return df_temp

def filter_by_condition(df:pd.DataFrame,envar:dict,time:str=None) -> pd.DataFrame | None:
    '''
    專門為了這個應用程式做的篩選器，會輸出經由envar篩選器篩過的df
    '''
    filter_df = df

    if time is not None:
        #將輸入的時間做為篩選器進行篩選
        filter_df = find(filter_df,
                         condition='time',
                         condi_args=time)
    
    #從環境變數中讀取校區篩選器並套用
    if envar['filter_campus'] != "all":
        filter_df = find(filter_df,
                         condition="campus",
                         condi_args=envar['filter_campus'])
    
    #從環境變數中讀取課程類型篩選器並套用
    if envar['filter_type'] != []:
        filter_df = find(filter_df,
                            condition="type",
                            condi_args=get_types_from_ezs(envar['filter_type']))
    
    #從環境變數中讀取課程名稱關鍵字後套用
    if envar['filter_name'] != "":
        filter_df = find(filter_df,
                            condition="name",
                            condi_args=envar['filter_name'])
        
    #從環境變數中讀取教師名字後套用
    if envar['filter_teacher'] != "":
        filter_df = find(filter_df,
                            condition="teacher",
                            condi_args=envar['filter_teacher'])
    
    #若沒有搜尋結果，則將結果設為None
    if len(filter_df) == 0:
        filter_df = None
    
    return filter_df