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
    _month_num = date_time_obj.strftime('%m')
    _day = date_time_obj.strftime('%d')
   
    if asset == "DAX":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C ODIV "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P ODIV "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            _temp_num+=5
        print(df)
    if asset == "SPX":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"C0"+str((start_strike+_temp_num))+"000"
            if option_type == "PUT" or option_type == "put":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"P0"+str((start_strike+_temp_num))+"000"
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            if (start_strike+_temp_num) < 2800 or ((start_strike+_temp_num) >= 4600 and (start_strike+_temp_num) <= 5000):
                _temp_num+=200
                continue
            if (start_strike+_temp_num) == 2800 or ((start_strike+_temp_num) >= 4300 and (start_strike+_temp_num) < 4600):
                _temp_num+=100
                continue
            if (start_strike+_temp_num) >= 2900 and (start_strike+_temp_num) < 3350:
                _temp_num+=50
                continue
            if ((start_strike+_temp_num) >= 3350 and (start_strike+_temp_num) < 3425) or ((start_strike+_temp_num) >= 4250 and (start_strike+_temp_num) < 4300):
                _temp_num+=25
                continue
            if (start_strike+_temp_num) == 3425:
                _temp_num+=15
                continue
            if ((start_strike+_temp_num) >= 3440 and (start_strike+_temp_num) < 3470) or ((start_strike+_temp_num) >= 3480 and (start_strike+_temp_num) < 3510) or ((start_strike+_temp_num) >= 4180 and (start_strike+_temp_num) < 4220) or ((start_strike+_temp_num) >= 4230 and (start_strike+_temp_num) < 4250):
                _temp_num+=10
                continue
            if ((start_strike+_temp_num) >= 3470 and (start_strike+_temp_num) < 3480) or ((start_strike+_temp_num) >= 3510 and (start_strike+_temp_num) < 4180) or ((start_strike+_temp_num) >= 4220 and (start_strike+_temp_num) < 4230):
                _temp_num+=5
                continue


            
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
                _name = "C OEXD "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P OEXD "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str(option_type).upper()] 
            if (start_strike+_temp_num) < 80 or ((start_strike+_temp_num) >= 85 and (start_strike+_temp_num) < 100):
                _temp_num+=5
                continue
            if (start_strike+_temp_num) == 80 or (start_strike+_temp_num) == 132:
                _temp_num+=3
                continue
            if (start_strike+_temp_num) == 83 or (start_strike+_temp_num) == 100 or (start_strike+_temp_num) == 110 or (start_strike+_temp_num) == 130:
                _temp_num+=2
                continue
            if (start_strike+_temp_num) >= 102 and (start_strike+_temp_num) < 110:
                _temp_num+=1
                continue
            if (start_strike+_temp_num) >= 112 and (start_strike+_temp_num) < 125:
                _temp_num+=1
                continue
            if (start_strike+_temp_num) == 125 or (start_strike+_temp_num) == 135:
                _temp_num+=5
                continue
            if (start_strike+_temp_num) == 140:
                _temp_num+=10
                continue
        print(df)

    
getSymbols("SPX","23/06/22",4145,23,"call")
    