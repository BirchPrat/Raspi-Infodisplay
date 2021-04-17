#Useful functions

def time_converter(sec_input):
    """returns a timestamp in from time module into H:M:S and days"""
    try:
        mins = sec_input // 60
        sec = sec_input % 60
        hours = mins // 60
        mins = mins % 60
        days = round(hours / 24, 3)
      
        return [f"{int(hours)}:{int(mins)}:{int(sec)}", days]
    
    except:
        return none
