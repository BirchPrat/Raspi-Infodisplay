#Useful functions

def time_converter(sec_input):
    """returns a timestamp in from time module into H:M:S"""
    try:
        mins = sec_input // 60
        sec = sec_input % 60
        hours = mins // 60
        mins = mins % 60
      
        return f"{int(hours)}:{int(mins)}:{int(sec)}"
    
    except:
        return none
