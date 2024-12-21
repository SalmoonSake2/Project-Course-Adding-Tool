'''
app.py

author:

Salmoon Sake
Azusa Kaze
-------------------------------------------------------------------------------
軟體本身
'''

import os
import threading
from tkinter import PhotoImage
from typing import Callable

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.validation import add_regex_validation
from pandas import DataFrame, isna

from libs.course_fetcher.fetch import check_timetable_update
from libs.course_fetcher.fetch import get_data_from_index
from libs.course_fetcher.fetch import get_acysem
from libs.extract import filter_by_condition
from libs.interface.colormapping import COLORMAPPING
from libs.interface.ym_mapping import get_campus
from libs.interface.ym_mapping import get_building_string
from libs.interface.ym_mapping import get_campus_id_from_cname
from libs.interface.ym_mapping import get_cname_from_campus_id
from libs.interface.ym_mapping import NYCU_CAMPUSES, NYCU_TIME_SLOTS,NYCU_DAYS,NYCU_TIMES,EZ_TYPE
from libs.interface.get_time_slot import get_time_slot
from libs.interface.stringutil import listring
from libs.interface.stringutil import autonl
import libs.interface.locale_zh_tw as zh_tw
import libs.interface.locale_en_us as en_us

def gen_pos(master):
    '''
    獲取生成位置
    '''
    return (master.winfo_x()+200,master.winfo_y()+150)

class APP:
    '''
    用以作為應用程式架構的類
    '''
    def __init__(self) -> None:
        '''
        初始化應用程式
        '''
        self.window = ttk.Window(themename="darkly",
                                 resizable=(False,False),
                                 size=(1052,780))
        self.window.withdraw()

        self.var_setting()
        self.window.mainloop()
        
    def real_init(self) -> None:
        '''
        真正的起始位置，會在語言選擇完後被呼叫
        '''
        self.window.title(self.loc["NYCU_course_adding_system"])
        
        path = os.path.join(os.path.join(os.path.dirname(__file__),"../../../assets"),"icon.ico")
        
        #為了避免物件載入畫面時出現placing，將畫面暫時隱藏後再載入。
        self.window.withdraw()
        self.wideget_setting()
        self.window.wm_iconbitmap(bitmap=path)
        self.window.deiconify()

        #配置完成，開始工作。
        self.window.protocol("WM_DELETE_WINDOW",self.onCloseWindow)
        self.tick()

    def var_setting(self) -> None:
        '''
        設置環境變數
        '''

        #環境變數
        self.envar = dict()
        self.envar['has_check_timetable_update'] = False
        self.envar['has_read_excel'] = False
        self.envar['filter_campus'] = ["YM","GF"]
        self.envar['filter_type'] = []
        self.envar['filter_name'] = ""
        self.envar['filter_teacher'] = ""
        self.envar['is_selecting'] = False

        #保持引用的圖片
        self.images = []

        #用來儲存所有課程資訊
        self.df:DataFrame = [None]

        #用來讓不同thread的runtime可以同步的參數
        self.retrn = [0]

        self.time_table:dict = dict.fromkeys(NYCU_TIME_SLOTS)

        #當前學年

        data_path = "user_data"

        self.acy = get_acysem(data_path)[0]
        self.sem = get_acysem(data_path)[1]
        
        #設置語言
        self.lang = get_acysem(data_path)[2]

        #停止程式而非繼續後續的動作
        def onCloseLangWindow() -> None:
            import sys
            sys.exit()
        
        #設置語言鍵值對
        def locmapping() -> None:
            match self.lang:
                case "zh_tw":
                    self.loc = zh_tw.LOC
                case "en_us":
                    self.loc = en_us.LOC

        #設置語言並關閉視窗
        def set_lang(lang:str) -> None:
            with open("user_data","w",encoding="utf-8") as file:
                file.write(self.acy+","+self.sem+","+lang)
            
            self.lang = lang
            locmapping()
            self.lang_select_window.destroy()
            self.real_init()

        #尚未設置語言
        if self.lang == "x":
            self.lang_select_window = ttk.Toplevel(title="Select Your language",
                                                 size=(800,600),
                                                 resizable=(False,False),
                                                 transient=self.window)

            path = os.path.join(os.path.join(os.path.dirname(__file__),"../../../assets"),"icon.ico")
            self.lang_select_window.wm_iconbitmap(bitmap=path)
            self.lang_select_window.protocol("WM_DELETE_WINDOW",onCloseLangWindow)

            #配置物件
            self.create_photo("zh_tw")
            self.create_photo("en_us")

            ttk.Canvas(master=self.lang_select_window,height=120).pack()
            ttk.Label(master=self.lang_select_window,text="選擇你的語言",font="Arial 24").pack()
            ttk.Label(master=self.lang_select_window,text="Choose Your Language",font="Arial 12").pack(pady=10)

            self.lang_button_frame = ttk.Frame(master=self.lang_select_window)
            self.lang_button_frame.pack(pady=40)

            ttk.Button(master=self.lang_button_frame,image="zh_tw",style="outline",command=lambda x="zh_tw":set_lang(x)).pack(side="left",padx=80)
            ttk.Button(master=self.lang_button_frame,image="en_us",style="outline",command=lambda x="en_us":set_lang(x)).pack(side="left",padx=80)

            locmapping()
        
        #已經有語言了
        else:
            locmapping()
            self.real_init()

    def wideget_setting(self) -> None:
        '''
        對畫面物件進行配置
        '''
        #載入圖片
        self.create_photo("loading_background")
        self.create_photo("browse")

        #最上面的位置，篩選器提示列
        self.filter_frame = ttk.Frame(master=self.window, style=ttk.DARK)
        self.add_filter_btn = ttk.Button(master=self.filter_frame,
                                         text=self.loc["set_filter_condition"],
                                         style='seconady-link',
                                         command=self.add_filter_event
                                         )
        self.add_filter_btn.pack(side="left")

        self.browse_btn = ttk.Button(master=self.filter_frame,
                                     image="browse",
                                     command=self.browse_event)
        self.browse_btn.pack(side="left")
        
        #中間課表的位置，在資料載入前隱藏
        self.time_table_frame = ttk.Frame(master=self.window,style=ttk.PRIMARY)
        self.info_label = ttk.Label(master=self.window,text=self.loc["handling"])
        self.info_label.pack()
        
        self.create_timetable_widget(self.time_table_frame)

        #學年提示

        def switch_event() -> None:
            self.ask_acysem_window = ttk.Toplevel(title=self.loc["select_acysem"],
                                                  size=(370 if self.lang == "zh_tw" else 470,100),
                                                  resizable=(False,False),
                                                  position=gen_pos(self.window),
                                                  transient=self.window)
            
            ttk.Label(master=self.ask_acysem_window,text=self.loc["please_enter_acysem"]).grid(row=0,column=0,padx=10,pady=20)
            self.acysem_entry = ttk.Entry(master=self.ask_acysem_window,
                                          width=5)
            self.acysem_entry.grid(row=0,column=1,padx=10,pady=20)

            add_regex_validation(self.acysem_entry,r"^11\d{1}[12]$")

            def btn_event():

                import re

                string = self.acysem_entry.get()

                if not re.match(r"^11\d[12]$",string):return
                with open("user_data","w",encoding="utf-8") as file:
                    file.write(string[:3]+","+string[3:]+","+self.lang)
                
                import os
                import sys

                os.remove("timetableDate.xlsx")
                
                Messagebox.show_info(self.loc["contain_updated_reopen"],self.loc["info"],parent=self.ask_acysem_window,alert=True)
                sys.exit()

            self.acysem_confirm_btn = ttk.Button(master=self.ask_acysem_window,
                                                 text=self.loc["confirm"],
                                                 command=lambda:btn_event())
            self.acysem_confirm_btn.grid(row=0,column=2,padx=10,pady=20)
            
        self.acysem_frame = ttk.Frame(master=self.window)
        self.acysem_label = ttk.Label(master=self.acysem_frame,text=self.loc["acysem_now"]+self.acy+self.loc["acy"]+self.loc[self.sem]+self.loc["semester"])
        self.acysem_label.pack(side="left")
        self.acysem_btn = ttk.Button(master=self.acysem_frame,
                                     text=self.loc["switch"],
                                     style="info-link",
                                     command=switch_event)
        self.acysem_btn.pack(side="left")
        
        #分隔線
        ttk.Canvas(master=self.acysem_frame,width=550 if self.lang == "zh_tw" else 425).pack(side="left")

        #學分提示
        ttk.Label(master=self.acysem_frame,text=self.loc["credit_now"]).pack(side="left")
        self.credit_count_var = ttk.IntVar(value=0)
        ttk.Label(master=self.acysem_frame,textvariable=self.credit_count_var).pack(side="left")

        #進度條的位置
        self.progressbar_obj = ttk.Floodgauge(master=self.window,
                                              bootstyle="info",
                                              font=(None,8),
                                              mask=self.loc["first_time_using_software"],
                                              length=1052)
        self.progressbar_obj.pack()

        #圖片

        self.image_frame = ttk.Frame(master=self.window)
        self.image_frame.pack()

        self.background_obj = ttk.Label(master=self.image_frame,
                                        image="loading_background")
        self.background_obj.pack(expand=True,fill="both",pady=120)

    def create_timetable_widget(self,frame:ttk.Frame) -> None:
        '''
        在指定的frame中建立課表介面物件
        '''

        DAYS = NYCU_DAYS
        TIMES = NYCU_TIMES

        #儲存課表物件的dict
        self.table_obj:dict[ttk.Button] = dict()

        #建立課表左側的時間欄
        for index, time in enumerate(TIMES):
            ttk.Label(master=frame,
                      text=time,
                      style=(ttk.INVERSE,ttk.PRIMARY)).grid(row=index+1,column=0,pady=2)

        #建立課表內容欄位
        for day_index, day in enumerate(DAYS):

            #建立課表上方星期列
            ttk.Label(master=frame,
                      text=day.upper(),
                      border=10,
                      style=(ttk.INVERSE,ttk.PRIMARY)).grid(row=0,column=day_index+1,padx=2)
            
            #為某天的每一個時間建立按鈕物件
            for time_index, time in enumerate(TIMES):
                
                #交互使用顏色(美觀)
                using_color = ttk.SECONDARY if time_index % 2 else ttk.LIGHT

                #建立按鈕事件
                btn_event = lambda time_slot = day + time: self.click_time_event(time_slot)

                #建立物件，並將其與事件綁定
                #注意！command = lambda f = btn_event: self.branch(f)不可以將 f = btn_event省略，否則
                #python將會失去對btn_event的引用，導致所有按鈕都指向Ud
                self.table_obj[day+time] = ttk.Button(master=frame,
                                                      width=12,
                                                      style=using_color,
                                                      command = lambda f = btn_event: self.branch(f)
                                                      )
                
                self.table_obj[day+time].grid(row=time_index+1,
                                              column=day_index+1,
                                              padx=2,
                                              pady=2
                                              )

    def click_time_event(self,time:str) -> None:
        '''
        點下課表時間按鈕後的事件
        '''

        #若正在進行選課，禁止更多操作
        if self.envar['is_selecting'] == True:
            return
        
        else:
            self.envar['is_selecting'] = True
        
        #顯示結果視窗
        self.show_result(filter_by_condition(self.df,self.envar,time),time)

    def show_result(self,df:DataFrame,time_slot:str=None) -> None:
        '''
        顯示結果的視窗，會將df的內容展示出來，如果有設定time_slot，則會將該
        時段已選的課程顯示在第一列。
        '''
        #若無結果，則跳視窗提示
        if df is None:
            self.retrn[0] = 1
            return 

        #建立結果視窗
        
        self.result_window = ttk.Toplevel(title=self.loc["select_course"],
                                          size=(1000,600),
                                          position=gen_pos(self.window),
                                          resizable=(True,False),
                                          transient=self.window,
                                          )
        
        self.result_window.protocol("WM_DELETE_WINDOW",self.onCloseResult)

        #用於紀錄範圍的變數
        VIEW_MAX = 200
        self.result_window.page = 1

        #將輸入的資料進行分割處理
        self.result_window.split_df = [df.iloc[i:i+VIEW_MAX] for i in range(0,len(df),VIEW_MAX)]
        using_df = self.result_window.split_df[0]

        self.refresh_scroll_frame(df=using_df,time_slot=time_slot)

    def refresh_scroll_frame(self,df:DataFrame,time_slot:str) -> None:
        '''
        以獲得的資料進行對ScrolledFrame的更新
        '''

        #提示文字
        self.result_info_label = ttk.Label(master=self.result_window,
                                           text=self.loc["searching"])
        self.result_info_label.pack()

        #頁面檢視器
        def last_page_event() -> None:
            if self.result_window.page != 1:
                self.result_window.page -= 1
                self.result_scroll_frame.container.destroy()
                self.page_view_frame.destroy()
                self.refresh_scroll_frame(self.result_window.split_df[self.result_window.page-1],
                                          time_slot if self.result_window.page == 1 else None)

            else:
                Messagebox.show_warning(message=self.loc["first_page"],title=self.loc["info"],alert=True)

        def next_page_event() -> None:
            if self.result_window.page != len(self.result_window.split_df):
                self.result_window.page += 1
                self.result_scroll_frame.container.destroy()
                self.page_view_frame.destroy()
                self.refresh_scroll_frame(self.result_window.split_df[self.result_window.page-1],
                                          time_slot if self.result_window.page == 1 else None)
            
            else:
                Messagebox.show_warning(message=self.loc["last_page"],title=self.loc["info"],alert=True)

        self.page_view_frame = ttk.Frame(master=self.result_window)

        self.last_page_btn = ttk.Button(master=self.page_view_frame,
                                        text=self.loc["go_last_page"],
                                        style="info-link",
                                        command=last_page_event)
        
        seperator = ttk.Canvas(master=self.page_view_frame,width=800 if self.lang == "zh_tw" else 770,height=10)

        self.next_page_btn = ttk.Button(master=self.page_view_frame,
                                        text=self.loc["go_next_page"],
                                        style="info-link",
                                        command=next_page_event)

        self.last_page_btn.grid(row=0,column=0)
        seperator.grid(row=0,column=1)
        self.next_page_btn.grid(row=0,column=2)


        #滾動式選單
        self.result_scroll_frame = ScrolledFrame(master=self.result_window)

        offset = 1

        #確認該時段有無課程，如果有則插入一個退選按鈕及課程資料
        if time_slot is not None:
            if self.time_table[time_slot] is not None:
                
                cos_data_frame = ttk.Labelframe(master=self.result_scroll_frame,
                                                text=self.loc["course_info"])
                cos_data_frame.grid(row=0,
                                    column=0,
                                    sticky="w",
                                    padx=10,
                                    pady=10,
                                    columnspan=10)

                cos_data = get_data_from_index(self.df,self.time_table[time_slot])

                #類型的字串需要進行本地化處理
                cos_type_string = ""
                if not isinstance(cos_data['brief'],float):
                    type_list = cos_data['brief'].split(",")
                    
                    for n,x in enumerate(type_list):
                        if n != 0:
                            cos_type_string += ", "
                        cos_type_string += self.loc[x]

                label_formats = (self.loc['course_name']+
                                 (cos_data['cos_cname'] if self.lang == "zh_tw" else cos_data['cos_ename']),
                                self.loc["course_type"]+cos_type_string,
                                self.loc["course_no"]+str(cos_data['cos_id']),
                                self.loc["permanent_id"]+cos_data['index'],
                                self.loc["student_limit"]+str(cos_data['num_limit'] if cos_data['num_limit'] != 9999 else self.loc["no_limit"]),
                                self.loc["course_credit"]+str(cos_data['cos_credit']),
                                self.loc["hour_per_week"]+str(cos_data['cos_hours']),
                                self.loc["course_teacher"]+autonl(str(cos_data['teacher'])),
                                self.loc["course_loaction"]+get_building_string(cos_data['cos_time'],self.lang),
                                self.loc["memo"]+(autonl(cos_data['memo'] if not isna(cos_data['memo']) else '')),
                                )

                #敘述內容
                for label_format in label_formats:
                    ttk.Label(master=cos_data_frame,text=label_format,width=90).pack(anchor="w")

                outline_url = f"https://timetable.nycu.edu.tw/?r=main/crsoutline&Acy={cos_data['acy']}&Sem={cos_data["sem"]}&CrsNo={cos_data["cos_id"]}&lang={"zh-tw" if self.lang == "zh_tw" else "en-us"}"

                if not isna(cos_data['crsoutline_type']):
                    ttk.Button(master=cos_data_frame,
                            text= self.loc["click_me_see_outline"],
                            style="link",
                            command=lambda link = outline_url:self.goToLink(link),
                            cursor="hand2").pack(anchor="w")

                #連結是個按鈕
                if not isna(cos_data['URL']):
                    ttk.Button(master=cos_data_frame,
                            text=self.loc["link"] + (cos_data['URL'] if not isna(cos_data['URL']) else ''),
                            style="link",
                            command=lambda link = cos_data['URL']:self.goToLink(link),
                            cursor="hand2").pack(anchor="w")
                
                #退選按鈕
                drop_btn = ttk.Button(master=cos_data_frame,
                                    text=self.loc["drop"],
                                    style="danger-outline",
                                    width=18,
                                    command=lambda x = time_slot:self.drop_event(x))
                drop_btn.pack(anchor="e",padx=5,pady=5)
                offset = 2

        #課程名稱
        for index,name in enumerate(df['cos_cname'] if self.lang == "zh_tw" else df["cos_ename"]):

            cos_index = df['index'].iat[index]
            select_event = lambda cos = cos_index:self.select_course_event(cos)

            btn = ttk.Button(master=self.result_scroll_frame,
                            text=name,
                            style="default-link",
                            width=18,
                            command=select_event)
            
            btn.grid(row=index+offset,
                    column=0,
                    sticky="w")
        
        #教師
        for index,name in enumerate(df['teacher']):

            #針對名字過長的欄位進行簡化
            #因為有老師的名字叫做1.0因此我需要寫一個防禦程式...幹
            if isinstance(name,str):
                if len(name) > 7:
                    name = name.split(self.loc["comma"])[0] + self.loc["and_others"]

            ttk.Label(master=self.result_scroll_frame,
                    text=name,
                    width=14).grid(row=index+offset,
                                    column=1,
                                    sticky="w",
                                    padx=5)
            
        #校區
        for index, timestring in enumerate(df['cos_time']):

            #獲取校區
            campuses = get_campus(timestring)

            #若為純線上課程，直接跳過
            if campuses is None: continue

            #建立框架
            campus_frame = ttk.Frame(master=self.result_scroll_frame)
            campus_frame.grid(row=index+offset,
                            column=2,
                            sticky="w",
                            padx=5)
            
            for campus in campuses:
                ttk.Label(master=campus_frame,
                        text=self.loc[campus]).pack(side="left",padx=3)
            
        #類型
        for index,cos_type in enumerate(df['brief']):
            
            #若查無資訊，直接跳過
            if isna(cos_type):continue

            #建立框架，比較好管理物件
            types_frame = ttk.Frame(master=self.result_scroll_frame)
            types_frame.grid(row=index+offset,
                            column=3,
                            sticky="w",
                            padx=5)

            #將每種屬性個別上色
            types = cos_type.split(",")

            #這不是錯字，是為了避免使用到python的關鍵字
            for l_index,tyqe in enumerate(types):
                label_obj = ttk.Label(master=types_frame,
                                    text=self.loc[types[l_index]],
                                    style=(ttk.INVERSE,COLORMAPPING[tyqe]))
                label_obj.pack(side="right",padx=3)

        self.result_info_label.destroy()
        self.page_view_frame.pack()
        self.result_scroll_frame.pack(expand=True,fill="both")

    def select_course_event(self,cos_index:str) -> None:
        '''
        選下去的事件處理
        '''

        #得到該課程的全部資訊
        cos_data = get_data_from_index(self.df,cos_index)

        #解析時段
        time_slots = get_time_slot(cos_data['cos_time'])

        #依序檢查新選課時段是否衝突
        conflict_coses = []
        conflict_cos_name = []

        for time_slot in time_slots:

            #若時段衝突
            if self.time_table[time_slot] != None:

                #紀錄衝突的課程
                conflcit_cos = self.time_table[time_slot]

                #只記錄尚未紀錄的
                if conflcit_cos not in conflict_coses:
                    conflict_coses.append(self.time_table[time_slot])
                    conflict_cos_name.append(get_data_from_index(self.df,conflcit_cos)["cos_cname"])
        
        #若存在衝突課程，發出提示
        if len(conflict_coses) != 0:

            resp = Messagebox.okcancel(message=self.loc["this_course_conflict_with"] + listring(conflict_cos_name),
                                       title=self.loc["course_conflict"],
                                       alert=True,
                                       parent=self.window)

            #若選擇yes，則將列表中的課程從課表移除
            if resp == "OK":
                for time_slot, cos in self.time_table.items():
                    if cos in conflict_coses:
                        self.time_table[time_slot] = None

            #若選擇no，則取消操作並退出
            else: return
        
        #將課程填入課表
        for time_slot in time_slots:
            self.time_table[time_slot] = cos_index
        
        #刷新畫面

        all_time_slots = NYCU_TIME_SLOTS

        for time_slot in all_time_slots:

            #對於沒有資料的格子，顯示空即可
            if self.time_table[time_slot] is None:
                show_text = ""

            else:
                cos_data = get_data_from_index(df=self.df,
                                                index=self.time_table[time_slot])
                show_text = cos_data['cos_cname'] if self.lang == "zh_tw" else cos_data['cos_ename']
            
            self.table_obj[time_slot].config(text=show_text)
        
        self.update_credit_sum()

        #關閉視窗
        try:
            self.result_window.destroy()
            self.envar["is_selecting"] = False
        except:
            ...

    def drop_event(self,time_slot:str) -> None:
        '''
        退選按鈕的事件
        '''
        time_slots = get_time_slot(get_data_from_index(self.df,self.time_table[time_slot])["cos_time"])

        #依序將退選的課表進行資料、畫面更新
        for time_slot in time_slots:
            self.time_table[time_slot] = None
            self.table_obj[time_slot].config(text="")
        
        self.update_credit_sum()
        
        try:
            self.result_window.destroy()
            self.envar["is_selecting"] = False
        except:
            ...

    def update_credit_sum(self) -> None:
        '''
        更新學分總和
        '''
        credit_sum = 0
        cos_list = []
        for time_index in self.time_table:
            cos_index = self.time_table[time_index]
            if cos_index is not None and cos_index not in cos_list:
                credit_sum += get_data_from_index(self.df,cos_index)["cos_credit"]
                cos_list.append(cos_index)
        
        self.credit_count_var.set(credit_sum)

    def add_filter_event(self) -> None:
        '''
        設置篩選器事件
        '''

        #建立視窗
        self.filter_window = ttk.Toplevel(title=self.loc["set_filter_condition"],
                                          size=(630,320 if self.lang == "zh_tw" else 380),
                                          resizable=(False,False),
                                          position=gen_pos(self.window),
                                          transient=self.window)

        #校區篩選器
        self.campus_filter_frame = ttk.Labelframe(master=self.filter_window,
                                                  text=self.loc["campus"])
        
        self.campus_check_btn = dict.fromkeys(NYCU_CAMPUSES)
        self.campus_check_var = dict.fromkeys(NYCU_CAMPUSES)

        for p_index, check_btn_index in enumerate(self.campus_check_btn):
            
            self.campus_check_var[check_btn_index] = ttk.BooleanVar(name=check_btn_index)

            check_btn = ttk.Checkbutton(master=self.campus_filter_frame,
                                        style="round-toggle",
                                        text=self.loc[check_btn_index],
                                        variable=self.campus_check_var[check_btn_index],
                                        onvalue=True,
                                        offvalue=False)
            
            #根據語言調整排版
            if self.lang == "zh_tw":
                check_btn.grid(row=0,column=p_index,padx=10,pady=10,sticky="w")
            
            else:
                check_btn.grid(row=p_index//3,column=p_index%3,padx=10,pady=10,sticky="w")

            self.campus_check_btn[check_btn_index] = check_btn

        self.campus_filter_frame.pack(anchor="w",padx=10,pady=10)

        #類別篩選器
        self.type_filter_frame = ttk.Labelframe(master=self.filter_window,
                                                  text=self.loc["type"])

        self.type_check_btn = dict.fromkeys(EZ_TYPE)
        self.type_check_var = dict.fromkeys(EZ_TYPE)

        for index, check_btn_index in enumerate(self.type_check_btn):

            self.type_check_var[check_btn_index] = ttk.BooleanVar(name=check_btn_index)

            check_btn = ttk.Checkbutton(master=self.type_filter_frame,
                                        style="info-round-toggle",
                                        text=self.loc[check_btn_index],
                                        variable=self.type_check_var[check_btn_index],
                                        onvalue=True,
                                        offvalue=False)
            
            check_btn.grid(row=index//3,column=index%3,padx=10,pady=10,sticky="w")
            self.type_check_btn[check_btn_index] = check_btn
        
        self.type_filter_frame.pack(anchor="w",padx=10,pady=10)

        self.entry_frame = ttk.Frame(master=self.filter_window)
        self.entry_frame.pack(anchor="w",padx=10,pady=10)

        #課程名稱
        self.name_filter_frame = ttk.LabelFrame(master=self.entry_frame,
                                                text=self.loc["course_name_keyword"])
        
        self.name_entry_var = ttk.StringVar()
        self.name_entry = ttk.Entry(master=self.name_filter_frame,width=20,textvariable=self.name_entry_var)
        self.name_entry.pack(side="left",padx=10,pady=10)

        self.name_filter_frame.pack(side="left")

        #教師名稱
        self.teacher_filter_frame = ttk.LabelFrame(master=self.entry_frame,
                                                text=self.loc["teacher"])
        self.teacher_entry_var = ttk.StringVar()
        self.teacher_entry = ttk.Entry(master=self.teacher_filter_frame,width=12,textvariable=self.teacher_entry_var)
        self.teacher_entry.pack(side="left",padx=10,pady=10)

        self.teacher_filter_frame.pack(side="left",padx=20)
        
        #按鈕

        self.confirm_filter_btn = ttk.Button(master=self.entry_frame,
                                             text=self.loc["confirm"],
                                             command=self.confirm_filter_event)
        self.confirm_filter_btn.pack(side="right",padx=0)

        self.reset_filter_btn = ttk.Button(master=self.entry_frame,
                                           text=self.loc["reset"],
                                           style="primary-outline",
                                           command=self.reset_filter_event)
        self.reset_filter_btn.pack(side="right",padx=10)

        #讀取環境變數，將物件(被動)與變數同步

        #校區的同步
        for campus in self.envar["filter_campus"]:
            self.campus_check_btn[get_cname_from_campus_id(campus)].invoke()

        #類別的同步
        for tyqe in self.envar["filter_type"]:
            self.type_check_btn[tyqe].invoke()

        #名稱的同步
        self.name_entry_var.set(self.envar["filter_name"])

        #教師的同步
        self.teacher_entry_var.set(self.envar["filter_teacher"])

    def reset_filter_event(self) -> None:
        '''
        按下重設篩選器的事件
        '''

        #將變數重設
        self.envar['filter_campus'] = ["YM","GF"]
        self.envar['filter_type'] = []
        self.envar["filter_name"] = ""
        self.envar["filter_teacher"] = ""

        #將物件配合變數切換

        #校區的同步
        for campus in NYCU_CAMPUSES:
            #如果內部變數狀態與物件狀態不一致，切換按鈕狀態
            if (get_campus_id_from_cname(campus) in self.envar["filter_campus"]) != self.campus_check_var[campus].get():
                self.campus_check_btn[campus].invoke()
        
        #類別的同步
        for ez_type in EZ_TYPE:
            if (ez_type in self.envar["filter_type"]) != self.type_check_var[ez_type].get():
                self.type_check_btn[ez_type].invoke()
        
        #課程名稱的同步
        self.name_entry_var.set(self.envar["filter_name"])

        #教師名稱的同步
        self.teacher_entry_var.set(self.envar["filter_teacher"])

    def confirm_filter_event(self) -> None:
        '''
        按下確定篩選器的事件
        '''

        #依序讀取配件並將環境變數設置

        #校區
        self.envar['filter_campus'] = []

        for campus_var_index in self.campus_check_var:
            
            #如果該配件設定為False，直接跳過
            if not self.campus_check_var[campus_var_index].get():
                continue

            self.envar['filter_campus'].append(get_campus_id_from_cname(campus_var_index))
        
        #類型
        self.envar['filter_type'] = []

        for type_var_index in self.type_check_var:
            
            #如果該配件設定為False，直接跳過
            if not self.type_check_var[type_var_index].get():
                continue

            self.envar['filter_type'].append(type_var_index)
        
        #名稱
        self.envar["filter_name"] = self.name_entry.get()

        #教師
        self.envar["filter_teacher"] = self.teacher_entry.get()

        #關閉視窗
        self.filter_window.destroy()

    def browse_event(self) -> None:
        '''
        透過瀏覽器搜尋的事件
        '''
        event = lambda:self.show_result(filter_by_condition(self.df,self.envar))
        self.branch(event)

    def branch(self,f:Callable) -> None:
        '''
        用於產生新的threading以避免主進程(介面)的無響應
        '''
        threading.Thread(target=f,daemon=True).start()
    
    def tick(self) -> None:
        '''
        用於軟體每刻(50ms)檢查的操作
        '''
        
        #尚未嘗試下載課表，建立thread來執行
        if self.envar['has_check_timetable_update'] == False:
            
            #如果將變數設為單純的0，那麼資料類型為immutable的，將難以在thread中對其進行操作
            self.progress_var = [0]
            self.last_progress = [0]

            self.branch(lambda:check_timetable_update(self.progress_var,
                                                      self.progressbar_obj,
                                                      self.df))
            self.envar['has_check_timetable_update'] = True

        #進度條畫面更新
        if self.progress_var != self.last_progress:
            self.progressbar_obj.step(6.25)
            self.last_progress = self.progress_var[:]
        
        #將下載好的課表進行預處理(對不起了Kaze，這部分我寫了一個屎代碼，但我一時間想不到一個好主意)
        #簡單說就是將用於儲存的項目提取出來，這涉及上述的immutable的問題。
        if not self.envar['has_read_excel']:
            if self.df[0] is not None:
                self.df = self.df[0]
                self.envar['has_read_excel'] = True

                #將課表啟用
                self.info_label.pack_forget()
                self.image_frame.pack_forget()

                #progress_bar的forget寫在fetch.py中
                self.filter_frame.pack(anchor="w")
                self.time_table_frame.pack()
                self.acysem_frame.pack(side="left",padx=10)

        #runtime回傳1代表需要顯示messagebox提示查無課程
        if self.retrn[0] == 1:
            self.retrn[0] = 0
            Messagebox.show_warning(message=self.loc["course_not_found"],
                                    title=self.loc["info"],
                                    parent=self.window,
                                    alert=True)
            
            self.envar["is_selecting"] = False
            
        self.window.after(ms= 50,func= self.tick)
    
    def onCloseWindow(self) -> None:
        '''
        關閉軟體的提示
        '''
        resp = Messagebox.okcancel(message=self.loc["confirm_to_exit"],
                                   title=self.loc["info"],
                                   parent=self.window)
        if resp == "OK":
            self.window.destroy()

    def onCloseResult(self) -> None:
        '''
        直接按x關閉結果的處理
        '''
        self.envar['is_selecting'] = False
        self.result_window.destroy()
    
    def goToLink(self,link:str) -> None:
        '''
        開啟指定網址
        '''
        import webbrowser as web

        resp = Messagebox.okcancel(self.loc["confirm_to_website"],self.loc["info"],True,self.result_window)

        if resp == "OK":web.open(link)

    def create_photo(self,file_name:str) -> None:
        '''
        建立圖檔
        '''
        self.images.append(PhotoImage(file=os.path.join(os.path.join(os.path.dirname(__file__),"../../../assets"),f"{file_name}.png"),name=file_name))
