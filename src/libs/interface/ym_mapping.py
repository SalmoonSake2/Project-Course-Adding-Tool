'''
ym_mapping.py

author:
Salmoon Sake
Akusa Kaze
-------------------------------------------------------------------------------
關於陽明交通大學的各種代號
'''
import re

YM_pattern = r'.*\[YM\].*'#陽明
GF_pattern = r'.*\[GF\].*'#光復(交大)
BA_pattern = r'.*\[BA\].*'#博愛
BM_pattern = r'.*\[BM\].*'#北門
GR_pattern = r'.*\[GR\].*'#歸仁
LJ_pattern = r'.*\[LJ\].*'#六家

def get_campus(cos_time_string:str) -> list[str] | None:
    '''
    擷取cos_time欄位中校區的代碼
    '''
    result = []
    if re.match(YM_pattern,cos_time_string):result.append("陽明")
    if re.match(GF_pattern,cos_time_string):result.append("光復")
    if re.match(BA_pattern,cos_time_string):result.append("博愛")
    if re.match(BM_pattern,cos_time_string):result.append("北門")
    if re.match(GR_pattern,cos_time_string):result.append("歸仁")
    if re.match(LJ_pattern,cos_time_string):result.append("六家")

    if len(result) == 0: return None
    
    return result

def get_building_string(cos_time_string:str,lang:str) -> str:
    '''
    獲取cos_time欄位中的資訊，並解析為人類可讀的文字
    '''
    if lang == "zh_tw":
        PATTERNS   = {'-YN': '於護理館', 
                  '-PhE':"於任意運動場",
                 '-YE': '於實驗大樓', 
                 '-YR': '於守仁樓', 
                 '-YS': '於醫學二館', 
                 '-YB': '於生醫工程館', 
                 '-YX': '於知行樓', 
                 '-YD': '於牙醫館', 
                 '-YK': '於傳統醫學大樓(甲棟)', 
                 '-YT': '於教學大樓', 
                 '-YM': '於醫學館', 
                 '-YL': '於圖書資源暨研究大樓', 
                 '-YA': '於活動中心', 
                 '-YH': '於致和樓', 
                 '-YC': '於生物醫學大樓', 
                 '-AS': '於中央研究院', 
                 '-PH': '於臺北榮民總醫院', 
                 '-CH': '於台中榮民總醫院', 
                 '-KH': '於高雄榮民總醫院', 
                 '-LI': '於實驗一館', 
                 '-BA': '於生科實驗館', 
                 '-BB': '於生科實驗二館', 
                 '-BI': '於賢齊館', 
                 '-EA': '於工程一館', 
                 '-EB': '於工程二館', 
                 '-EC': '於工程三館', 
                 '-ED': '於工程四館', 
                 '-EE': '於工程五館', 
                 '-EF': '於工程六館', 
                 '-MB': '於管理二館', 
                 '-SA': '於科學一館', 
                 '-SB': '於科學二館', 
                 '-SC': '於科學三館', 
                 '-AC': '於學生活動中心',  
                 '-AB': '於綜合一館地下室', 
                 '-HA': '於人社一館',  
                 '-HB': '於人社二館', 
                 '-HC': '於人社三館', 
                 '-CY': '於交映樓', 
                 '-EO': '於田家炳光電大樓', 
                 '-EV': '於環工館', 
                 '-CS': '於資訊技術服務中心', 
                 '-ES': '於電子資訊中心', 
                 '-CE': '於土木結構實驗室', 
                 '-AD': '於大禮堂', 
                 '-Lib': '於浩然圖書資訊中心', 
                 '-TA': '於會議室', 
                 '-TD': '於一般教室', 
                 '-TC': '於演講廳', 
                 '-CM': '於奇美樓', 
                 '-HK': '於客家大樓',
                 '-F': '於人社二館',
                 '-A': '於綜合一館',
                 '-C': '於竹銘館', 
                 '-E': '於教學大樓', 
                 '-M': '於管理館', 
                 "[YM]":"教室[陽明]",
                 "[GF]":"教室[光復]",#交大
                 "[BA]":"教室[博愛]",
                 "[BM]":"教室[北門]",
                 "[GR]":"教室[歸仁]",
                 "[LJ]":"教室[六家]",
                 "M":"週一",
                 "T":"週二",
                 "W":"週三",
                 "R":"週四",
                 "F":"週五",
                 "S":"週六",
                 "U":"週日",
                 "-":"於線上或未知地點"}
        
    else:
        PATTERNS   = {'-YN': ' at nursing building', 
                  '-PhE':" at any possible place for exercise",
                 '-YE': ' at experimental building', 
                 '-YR': ' at shouren building', 
                 '-YS': ' at medical building Ⅱ', 
                 '-YB': ' at biomedical engineering building', 
                 '-YX': ' at zhi xing building', 
                 '-YD': ' at dentistry building', 
                 '-YK': ' at traditional medical building', 
                 '-YT': ' at teaching building', 
                 '-YM': ' at medical building', 
                 '-YL': ' at library, information and research building', 
                 '-YA': ' at auditorium and activity center', 
                 '-YH': ' at zhi-he building', 
                 '-YC': ' at biomedical building', 
                 '-AS': ' at academia sinica', 
                 '-PH': ' at taipei veterans general hospital', 
                 '-CH': ' at taichung veterans general hospital', 
                 '-KH': ' at kaohsiung veterans general hospital', 
                 '-LI': ' at laboratory Hhll', 
                 '-BA': ' at biotech experiment building', 
                 '-BB': ' at biotech experiment building 2', 
                 '-BI': ' at bio-ict building', 
                 '-EA': ' at engineering building 1', 
                 '-EB': ' at engineering building 2', 
                 '-EC': ' at engineering building 3', 
                 '-ED': ' at engineering building 4', 
                 '-EE': ' at engineering building 5', 
                 '-EF': ' at engineering building 6', 
                 '-MB': ' at management building 2', 
                 '-SA': ' at science building 1', 
                 '-SB': ' at science building 2', 
                 '-SC': ' at science building 3', 
                 '-AC': ' at students activity center',  
                 '-AB': ' at assembly building 1 basement', 
                 '-HA': ' at humanities and social sciences building 1',  
                 '-HB': ' at humanities and social sciences building 2', 
                 '-HC': ' at humanities and social sciences building 3', 
                 '-CY': ' at cpt building', 
                 '-EO': ' at electro optical(tin ka ping photonic building）', 
                 '-EV': ' at environmental engineering building', 
                 '-CS': ' at information technology service center', 
                 '-ES': ' at microelectronics and information system research center', 
                 '-CE': ' at civil engineering lab', 
                 '-AD': ' at auditorium', 
                 '-Lib': ' at library and information center', 
                 '-TA': ' at conference room', 
                 '-TD': ' at classrooms', 
                 '-TC': ' at lecture hall', 
                 '-CM': ' at chi mei building', 
                 '-HK': ' at hakka building',
                 '-F': ' at humanities and social sciences building 2',
                 '-A': ' at assembly building 1',
                 '-C': ' at chu ming building', 
                 '-E': ' at education building', 
                 '-M': ' at management building 1', 
                 "[YM]":" classroom[ym]",
                 "[GF]":" classroom[gf]",#交大
                 "[BA]":" classroom[ba]",
                 "[BM]":" classroom[bm]",
                 "[GR]":" classroom[gr]",
                 "[LJ]":" classroom[lj]",
                 "M":"mon.",
                 "T":"tue.",
                 "W":"wed.",
                 "R":"thr.",
                 "F":"fri",
                 "S":"sat.",
                 "U":"sun.",
                 "-":" online or other places"}
    
    result = cos_time_string

    #依序從pattern中找尋可以替代的
    for pattern in PATTERNS:
        if pattern in result:
            result = result.replace(pattern,PATTERNS[pattern])
    
    return result

def get_campus_id_from_cname(cname:str) -> str:
    '''
    從校區中文名獲得校區代碼
    '''
    id = None
    match cname:
        case "陽明": id = "YM"
        case "光復": id = "GF"
        case "博愛": id = "BA"
        case "北門": id = "BM"
        case "歸仁": id = "GR"
        case "六家": id = "LJ"
    
    return id

def get_cname_from_campus_id(campus_id:str) -> str:
    '''
    從校區代碼獲得中文名
    '''
    id = None
    match campus_id:
        case "YM": id = "陽明"
        case "GF": id = "光復"
        case "BA": id = "博愛"
        case "BM": id = "北門"
        case "GR": id = "歸仁"
        case "LJ": id = "六家"
    return id

def get_types_from_ez(cos_type:str) -> list[str]:
    '''
    從簡易類型中獲取詳細類型
    '''
    value = [('通識校基本素養','通識跨院基本素養','基本素養-組織管理','基本素養-量性推理','基本素養-生命及品格教育','基本素養-批判思考'),
             ('領域課程-人文與美學','領域課程-個人、社會與文化','領域課程-社會中的科技與自然','領域課程-公民與倫理思考'),
             ('語言與溝通-英文','語言領域-英文'),
             ('語言與溝通-第二外語','語言與溝通-溝通表達','語言領域-中文(含寫作)'),
             ("程式相關",),#這逗點必須加上，不然會被自動變成純字串而非tuple
             ("體育",)]
    mapping = dict.fromkeys(EZ_TYPE)

    for index, ez_type in enumerate(mapping):
        mapping[ez_type] = value[index]
    
    return mapping[cos_type]

def get_types_from_ezs(cos_types:list[str]) -> list[str]:
    '''
    從簡易類型串列中獲取詳細類型
    '''
    result = []
    for cos_type in cos_types:
        result.extend(get_types_from_ez(cos_type))
    return result

#體育課用dep_id: OU9找出來

NYCU_CAMPUSES = ["陽明","光復","博愛","北門","歸仁","六家"]
NYCU_TIME_SLOTS = ['My', 'Mz', 'M1', 'M2', 'M3', 'M4', 'Mn', 'M5', 'M6', 'M7', 'M8', 'M9', 'Ma', 'Mb', 'Mc', 'Md', 'Ty', 'Tz', 'T1', 'T2', 'T3', 'T4', 'Tn', 'T5', 'T6', 'T7', 'T8', 'T9', 'Ta', 'Tb', 'Tc', 'Td', 'Wy', 'Wz', 'W1', 'W2', 'W3', 'W4', 'Wn', 'W5', 'W6', 'W7', 'W8', 'W9', 'Wa', 'Wb', 'Wc', 'Wd', 'Ry', 'Rz', 'R1', 'R2', 'R3', 'R4', 'Rn', 'R5', 'R6', 'R7', 'R8', 'R9', 'Ra', 'Rb', 'Rc', 'Rd', 'Fy', 'Fz', 'F1', 'F2', 'F3', 'F4', 'Fn', 'F5', 'F6', 'F7', 'F8', 'F9', 'Fa', 'Fb', 'Fc', 'Fd', 'Sy', 'Sz', 'S1', 'S2', 'S3', 'S4', 'Sn', 'S5', 'S6', 'S7', 'S8', 'S9', 'Sa', 'Sb', 'Sc', 'Sd', 'Uy', 'Uz', 'U1', 'U2', 'U3', 'U4', 'Un', 'U5', 'U6', 'U7', 'U8', 'U9', 'Ua', 'Ub', 'Uc', 'Ud']
NYCU_COS_TYPE = ['', '跨校區課程', '基礎服務學習', '通識核心課程', '核心通識-科技與社會', '通識校基本素養', '大學導師', '通識跨院基本素養', 'OCW', '品德教育', '語言與溝通-第二外語', '開放隨班附讀', '基本素養-組織管理', '音樂指導(個別指導費)', '專題演講', '遠距課程', '人權教育', '生命教育', '程式相關', '語言與溝通-英文','媒體資訊判讀', '領域課程-人文與美學','基本素養-量性推理', '核心通識-藝術與文化','大型展演', '一般實習', '實驗課程', '核心通識-哲學與心靈','核心通識-歷史與文明','智財權課程','寫作課程', '書報專題討論', '核心通識-倫理與道德思考','專業服務學習', '領域課程-個人、社會與文化','大學專題', '基本素養-生命及品格教育', '博雅選修通識','不支援核心', '領域課程-社會中的科技與自然','語言與溝通-溝通表達', '語言領域-中文(含寫作)', '性平相關課程', '基本素養-批判思考', '核心通識-社會與經濟', '語言領域-英文', '人文關懷', '社會參與', '領域課程-公民與倫理思考']
NYCU_DAYS = ("M","T","W","R","F","S","U")
NYCU_TIMES = ("y","z","1","2","3","4","n","5","6","7","8","9","a","b","c","d")
EZ_TYPE = ['基本素養',"領域課程","語言與溝通-英文","語言與溝通-其他","程式相關","體育"]