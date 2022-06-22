from re import L
import pandas as pd
from datetime import datetime

list_assets = [['SPX','CBOE'],['DAX','DTB'],['CL','NYSE'],['NG','NYMEX'],['VIX','CBOE'],['V2EU','DTB'],['STOXX','DTB']]


def getSymbols(asset, expiration, start_strike, number, option_type):
    df = pd.DataFrame(columns=['Name','Strike','Exchange','Type'])

    # date format as 21/01/22 (21 Jan 2022)
    date_time_obj = datetime.strptime(expiration, '%d/%m/%y')
    _year = date_time_obj.strftime('%y')
    _month = date_time_obj.strftime('%b')
    _day = date_time_obj.strftime('%d')
   
    if asset == "DAX":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C ODIV"+str(_month).upper()+str(_year)+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P ODIV "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            _temp_num+=5
        print(df)
    if asset == "SPX":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "SPXW "+str(_month).upper()+str(_year)+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P ODIV "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            _temp_num+=5
        print(df)
    if asset == "CL":
        pass
    if asset == "NG":
        pass
    if asset == "VIX":
        pass
    if asset == "V2EU":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C OVS2"+str(_month).upper()+str(_year)+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P OVS2 "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            if (start_strike+_temp_num) < 15:
                _temp_num+=0.5
                continue
            if (start_strike+_temp_num) >= 15 and (start_strike+_temp_num) < 30:
                _temp_num+=1
                continue
            if (start_strike+_temp_num) >= 30 and (start_strike+_temp_num) < 50:
                _temp_num+=2
                continue
            if (start_strike+_temp_num) >= 50 and (start_strike+_temp_num) < 100:
                _temp_num+=5
                continue
            if (start_strike+_temp_num) >= 100:
                _temp_num+=10
        print(df)
    if asset == "STOXX":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C OEXD"+str(_month).upper()+str(_year)+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P OEXD "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            if (start_strike+_temp_num) < 80:
                _temp_num+=5
                continue
            if (start_strike+_temp_num) == 80:
                _temp_num+=3
                continue
            if (start_strike+_temp_num) == 83:
                _temp_num+=2
                continue
            if (start_strike+_temp_num) >= 85 and (start_strike+_temp_num) < 100:
                _temp_num+=5
                continue
            if (start_strike+_temp_num) == 100:
                _temp_num+=2
                continue
            if (start_strike+_temp_num) >= 102 and (start_strike+_temp_num) < 110:
                _temp_num+=1
                continue
            if (start_strike+_temp_num) == 110:
                _temp_num+=2
                continue
            if (start_strike+_temp_num) >= 112 and (start_strike+_temp_num) < 125:
                _temp_num+=1
                continue
            if (start_strike+_temp_num) == 125:
                _temp_num+=5
                continue
            if (start_strike+_temp_num) == 130:
                _temp_num+=2
                continue
            if (start_strike+_temp_num) == 132:
                _temp_num+=3
                continue
            if (start_strike+_temp_num) == 135:
                _temp_num+=5
                continue
            if (start_strike+_temp_num) == 140:
                _temp_num+=10
                continue
        print(df)

    
getSymbols("STOXX","15/09/23",40,42,"call")
    