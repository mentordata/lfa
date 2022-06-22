from re import L
import pandas as pd
from datetime import datetime

list_assets = [['SPX','CBOE'],['DAX','DTB'],['CL','NYSE'],['NG','NYMEX'],['VIX','CBOE'],['V2EU','DTB'],['STOXX','DTB']]


def getSymbols(asset, expiration, start_strike, number, option_type):
    df = pd.DataFrame(columns=['Name','Strike','Exchange','Type'])

    # date format as 2022.06.23 (23 JUN 2022)
    date_time_obj = datetime.strptime(expiration, '%Y.%m.%d')
    
    _year = date_time_obj.strftime('%y')
    _month = date_time_obj.strftime('%b')
    _month_num = date_time_obj.strftime('%m')
    _day = date_time_obj.strftime('%d')
   
    

    if asset == "DAX":
        _dax4_exp_dates = ["2022-06-24"]
        _dax1_exp_dates = ["2022-07-01"]
        _dax2_exp_dates = ["2022-07-08"]
        _dax5_exp_dates = ["2022-07-29"]
        _dax_exp_dates = ["2022-07-15","2022-08-19","2022-09-16","2022-12-16","2023-3-17"]
        if date_time_obj.strftime('%Y-%m-%d') in _dax_exp_dates:
                _dex_desc = "ODX"
                print(_dex_desc)
        if date_time_obj.strftime('%Y-%m-%d') in _dax1_exp_dates:
                _dex_desc = "ODX1"
                print(_dex_desc)
        if date_time_obj.strftime('%Y-%m-%d') in _dax2_exp_dates:
                _dex_desc = "ODX2"
                print(_dex_desc)
        if date_time_obj.strftime('%Y-%m-%d') in _dax4_exp_dates:
                _dex_desc = "ODX4"
                print(_dex_desc)
        if date_time_obj.strftime('%Y-%m-%d') in _dax5_exp_dates:
                _dex_desc = "ODX5"
                print(_dex_desc)
        _temp_num = 0
        _curr_strike = start_strike+_temp_num
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C "+str(_dex_desc).upper()+" "+str(_month).upper()+" "+str(_year)+" "+str((_curr_strike))
            if option_type == "PUT" or option_type == "put":
                _name = "P "+str(_dex_desc).upper()+" "+str(_month).upper()+" "+str(_year)+" "+str((_curr_strike))
            
            df.loc[i] = [_name,(_curr_strike),"DTB",str("OPT").upper()] 
            
            if date_time_obj.strftime('%Y-%m-%d') == "2022-06-24" or date_time_obj.strftime('%Y-%m-%d') == "2022-07-01" or date_time_obj.strftime('%Y-%m-%d') == "2022-07-08" or date_time_obj.strftime('%Y-%m-%d') == "2022-07-29":
                if (_curr_strike) >= 11800:
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-07-15":
                if (_curr_strike) == 8000:
                    _temp_num+=1000
                    continue
                if (_curr_strike) >= 9000 and (_curr_strike) < 11800:
                    _temp_num+=200
                    continue
                if (_curr_strike) >= 11800:
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-08-19":
                if (_curr_strike) == 15900:
                    _temp_num+=100
                    continue
                if ((_curr_strike) >= 8000 and (_curr_strike) < 11800) or ((_curr_strike) >= 16000 and (_curr_strike) < 18000):
                    _temp_num+=200
                    continue
                if (_curr_strike) >= 11800 and (_curr_strike) < 15900:
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-09-16": # to fix
                if (_curr_strike) == 2000:
                    _temp_num+=2500
                    continue
                if (_curr_strike) >= 4500 and (_curr_strike) < 10000:
                    _temp_num+=500
                    continue
                if ((_curr_strike) >= 10000 and (_curr_strike) < 10800) or ((_curr_strike) >= 16000 and (_curr_strike) < 18000):
                    _temp_num+=200
                    continue
                
            

        print(df)
    if asset == "SPX":
        _temp_num = 0
        _curr_strike = start_strike+_temp_num
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"C0"+str((_curr_strike))+"000"
            if option_type == "PUT" or option_type == "put":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"P0"+str((_curr_strike))+"000"
            
            df.loc[i] = [_name,(_curr_strike),"CBOE",str("OPT").upper()] 
            if (_curr_strike) < 2800 or ((_curr_strike) >= 4600 and (_curr_strike) <= 5000):
                _temp_num+=200
                continue
            if (_curr_strike) == 2800 or ((_curr_strike) >= 4300 and (_curr_strike) < 4600):
                _temp_num+=100
                continue
            if (_curr_strike) >= 2900 and (_curr_strike) < 3350:
                _temp_num+=50
                continue
            if ((_curr_strike) >= 3350 and (_curr_strike) < 3425) or ((_curr_strike) >= 4250 and (_curr_strike) < 4300):
                _temp_num+=25
                continue
            if (_curr_strike) == 3425:
                _temp_num+=15
                continue
            if ((_curr_strike) >= 3440 and (_curr_strike) < 3470) or ((_curr_strike) >= 3480 and (_curr_strike) < 3510) or ((_curr_strike) >= 4180 and (_curr_strike) < 4220) or ((_curr_strike) >= 4230 and (_curr_strike) < 4250):
                _temp_num+=10
                continue
            if ((_curr_strike) >= 3470 and (_curr_strike) < 3480) or ((_curr_strike) >= 3510 and (_curr_strike) < 4180) or ((_curr_strike) >= 4220 and (_curr_strike) < 4230):
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
        _curr_strike = start_strike+_temp_num
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C OVS2"+str(_month).upper()+str(_year)+str((_curr_strike))
            if option_type == "PUT" or option_type == "put":
                _name = "P OVS2 "+str(_month).upper()+" "+str(_year)+" "+str((_curr_strike))
            
            df.loc[i] = [_name,(_curr_strike),"DTB",str("OPT").upper()] 
            if (_curr_strike) < 15:
                _temp_num+=0.5
                continue
            if (_curr_strike) >= 15 and (_curr_strike) < 30:
                _temp_num+=1
                continue
            if (_curr_strike) >= 30 and (_curr_strike) < 50:
                _temp_num+=2
                continue
            if (_curr_strike) >= 50 and (_curr_strike) < 100:
                _temp_num+=5
                continue
            if (_curr_strike) >= 100:
                _temp_num+=10
        print(df)
    if asset == "STOXX":
        _temp_num = 0
        _curr_strike = start_strike+_temp_num
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C OEXD "+str(_month).upper()+" "+str(_year)+" "+str((_curr_strike))
            if option_type == "PUT" or option_type == "put":
                _name = "P OEXD "+str(_month).upper()+" "+str(_year)+" "+str((_curr_strike))
            
            df.loc[i] = [_name,(_curr_strike),"DTB",str(option_type).upper()] 
            if (_curr_strike) < 80 or ((_curr_strike) >= 85 and (_curr_strike) < 100):
                _temp_num+=5
                continue
            if (_curr_strike) == 80 or (_curr_strike) == 132:
                _temp_num+=3
                continue
            if (_curr_strike) == 83 or (_curr_strike) == 100 or (_curr_strike) == 110 or (_curr_strike) == 130:
                _temp_num+=2
                continue
            if (_curr_strike) >= 102 and (_curr_strike) < 110:
                _temp_num+=1
                continue
            if (_curr_strike) >= 112 and (_curr_strike) < 125:
                _temp_num+=1
                continue
            if (_curr_strike) == 125 or (_curr_strike) == 135:
                _temp_num+=5
                continue
            if (_curr_strike) == 140:
                _temp_num+=10
                continue
        print(df)

    
getSymbols("DAX","2022.06.24",20,10,"call")
    