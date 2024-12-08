'''
get_time_slot.py

author:
Salmoon Sake
-------------------------------------------------------------------------------

用以將陽明的時段代號處理並分割
'''
def get_time_slot(time_slot_string:str) -> list[str]:
    '''
    用以將陽明的時段代號處理並分割
    '''
    space_time_strings = time_slot_string.split(",")

    result = []

    for space_time_string in space_time_strings:

        time_string = space_time_string.split("-")[0]
    
        valid_day_symbols = "MTWRFSU"

        cutboard = []
        last_index = 0

        for index, alphabelt in enumerate(time_string):
            if alphabelt in valid_day_symbols and index != 0:
                cutboard.append(time_string[last_index:index])
                last_index = index
        
        cutboard.append(time_string[last_index:len(time_string)])

        for day in cutboard:
            day_symbol = day[0]
            for time_slot in day[1:len(day)]:
                result.append(day_symbol+time_slot)
        
    return result

if __name__ == "__main__":
    x = get_time_slot("W567-YL402[YM],R567-YR101[YM]")
    print(x)