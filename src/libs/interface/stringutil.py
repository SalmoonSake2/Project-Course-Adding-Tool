'''
strutil.py

author:
Salmoon Sake
-------------------------------------------------------------------------------

字串實用工具們
'''

def listring(iterable) -> str:
    '''
    用來將iterable的內容轉為字串
    '''
    result = ""
    for element in iterable:
        result = result + str(element) + "、"
    
    return result.rstrip("、")

def autonl(string:str,n:int=45) -> str:
    '''
    自動換行
    '''
    result = ""
    counter = 0
    for char in string:
        result += char
        if char == "\n":
            counter = 0
        counter += 1
        if counter % n == 0 and counter != 0:
            result += "\n"
    
    return result
