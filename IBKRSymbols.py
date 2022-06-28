from calendar import setfirstweekday
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
                _dex_desc = "ODAX"
                print(_dex_desc)
        elif date_time_obj.strftime('%Y-%m-%d') in _dax1_exp_dates:
                _dex_desc = "ODX1"
                print(_dex_desc)
        elif date_time_obj.strftime('%Y-%m-%d') in _dax2_exp_dates:
                _dex_desc = "ODX2"
                print(_dex_desc)
        elif date_time_obj.strftime('%Y-%m-%d') in _dax4_exp_dates:
                _dex_desc = "ODX4"
                print(_dex_desc)
        elif date_time_obj.strftime('%Y-%m-%d') in _dax5_exp_dates:
                _dex_desc = "ODX5"
                print(_dex_desc)
        else:
            print("Provided expiration date is wrong.")
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "C "+str(_dex_desc).upper()+" "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            if option_type == "PUT" or option_type == "put":
                _name = "P "+str(_dex_desc).upper()+" "+str(_month).upper()+" "+str(_year)+" "+str((start_strike+_temp_num))
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str("OPT").upper()] 
            
            if date_time_obj.strftime('%Y-%m-%d') == "2022-06-24" or date_time_obj.strftime('%Y-%m-%d') == "2022-07-01" or date_time_obj.strftime('%Y-%m-%d') == "2022-07-08" or date_time_obj.strftime('%Y-%m-%d') == "2022-07-29":
                if (start_strike+_temp_num) >= 11800:
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-07-15":
                if (start_strike+_temp_num) == 8000:
                    _temp_num+=1000
                    continue
                if (start_strike+_temp_num) >= 9000 and (start_strike+_temp_num) < 11800:
                    _temp_num+=200
                    continue
                if (start_strike+_temp_num) >= 11800:
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-08-19":
                if (start_strike+_temp_num) == 15900:
                    _temp_num+=100
                    continue
                if ((start_strike+_temp_num) >= 8000 and (start_strike+_temp_num) < 11800) or ((start_strike+_temp_num) >= 16000 and (start_strike+_temp_num) < 18000):
                    _temp_num+=200
                    continue
                if (start_strike+_temp_num) >= 11800 and (start_strike+_temp_num) < 15900:
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-09-16":
                if (start_strike+_temp_num) == 2000:
                    _temp_num+=2500
                    continue
                if (start_strike+_temp_num) >= 4500 and (start_strike+_temp_num) < 10000:
                    _temp_num+=500
                    continue
                if ((start_strike+_temp_num) >= 10000 and (start_strike+_temp_num) < 10800) or ((start_strike+_temp_num) >= 17200 and (start_strike+_temp_num) < 20000):
                    _temp_num+=200
                    continue
                if ((start_strike+_temp_num) >= 10800 and (start_strike+_temp_num) < 11900) or ((start_strike+_temp_num) >= 14500 and (start_strike+_temp_num) < 17200):
                    _temp_num+=100
                    continue
                if ((start_strike+_temp_num) >= 11900 and (start_strike+_temp_num) < 14500):
                    _temp_num+=50
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2022-12-16":
                if (start_strike+_temp_num) == 2000:
                    _temp_num+=2500
                    continue
                if ((start_strike+_temp_num) >= 4500 and (start_strike+_temp_num) < 6500) or ((start_strike+_temp_num) >= 19000 and (start_strike+_temp_num) < 22000):
                    _temp_num+=500
                    continue
                if ((start_strike+_temp_num) >= 6500 and (start_strike+_temp_num) < 7000):
                    _temp_num+=300
                    continue
                if ((start_strike+_temp_num) >= 7000 and (start_strike+_temp_num) < 7400) or ((start_strike+_temp_num) >= 7600 and (start_strike+_temp_num) < 8400):
                    _temp_num+=200
                    continue
                if ((start_strike+_temp_num) >= 7400 and (start_strike+_temp_num) < 7600) or ((start_strike+_temp_num) >= 8400 and (start_strike+_temp_num) < 8600):
                    _temp_num+=100
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2023-03-17":
                if ((start_strike+_temp_num) >= 4500 and (start_strike+_temp_num) < 7000) or ((start_strike+_temp_num) >= 19000 and (start_strike+_temp_num) < 22000):
                    _temp_num+=500
                    continue
                if ((start_strike+_temp_num) >= 7000 and (start_strike+_temp_num) < 11000) or ((start_strike+_temp_num) >= 17600 and (start_strike+_temp_num) < 18400) or ((start_strike+_temp_num) >= 18600 and (start_strike+_temp_num) < 19000):
                    _temp_num+=200
                    continue
                if ((start_strike+_temp_num) >= 11000 and (start_strike+_temp_num) < 17600) or ((start_strike+_temp_num) >= 18400 and (start_strike+_temp_num) < 18600):
                    _temp_num+=100
                    continue
            if date_time_obj.strftime('%Y-%m-%d') == "2023-06-16":
                if (start_strike+_temp_num) == 2500:
                    _temp_num+=3500
                    continue
                if ((start_strike+_temp_num) == 2000 or ((start_strike+_temp_num) >= 18000 and (start_strike+_temp_num) < 22000)):
                    _temp_num+=500
                    continue
                if ((start_strike+_temp_num) >= 6000 and (start_strike+_temp_num) < 12000) or ((start_strike+_temp_num) >= 17000 and (start_strike+_temp_num) < 17400) or ((start_strike+_temp_num) >= 17600 and (start_strike+_temp_num) < 18000):
                    _temp_num+=200
                    continue
                if ((start_strike+_temp_num) >= 12000 and (start_strike+_temp_num) < 17000) or ((start_strike+_temp_num) >= 17400 and (start_strike+_temp_num) < 17600):
                    _temp_num+=100
                    continue
                

        print(df)
    if asset == "SPX":
        _temp_num = 0
        for i in range(number):
            if option_type == "CALL" or option_type == "call":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"C0"+str((start_strike+_temp_num))+"000"
            if option_type == "PUT" or option_type == "put":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"P0"+str((start_strike+_temp_num))+"000"
            
            df.loc[i] = [_name,(start_strike+_temp_num),"CBOE",str("OPT").upper()] 
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
            
            df.loc[i] = [_name,(start_strike+_temp_num),"DTB",str("OPT").upper()] 
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

    # function that takes start_strike as vector
def getVecSymbols(asset, expiration, start_strike, number, option_type):
    df = pd.DataFrame(columns=['Name','Strike','Exchange','Type'])
    
    # date format as 2022.06.23 (23 JUN 2022)
    date_time_obj = datetime.strptime(expiration, '%Y.%m.%d')
    
    _year = date_time_obj.strftime('%y')
    _month = date_time_obj.strftime('%b')
    _month_num = date_time_obj.strftime('%m')
    _day = date_time_obj.strftime('%d')
   
    

    if asset == "DAX":
        _dax_names = [["ODX4","2022-06-24"],
                     ["ODX1","2022-07-01"],
                     ["ODX2","2022-07-08"],
                     ["ODX5","2022-07-29"],
                     ["ODAX","2022-07-15"],
                     ["ODAX","2022-08-19"],
                     ["ODAX","2022-09-16"],
                     ["ODAX","2022-12-16"],
                     ["ODAX","2023-03-17"]]

        _date = date_time_obj.strftime('%Y-%m-%d') 
        _dax_desc = [t[0] for t in _dax_names if t[1] == _date ]

        _temp_num = 0
        for i in range(len(start_strike)):
            if option_type == "CALL" or option_type == "call":
                _name = "C "+str(_dax_desc[0]).upper()+" "+str(_month).upper()+" "+str(_year)+" "+str((start_strike[_temp_num]))
            if option_type == "PUT" or option_type == "put":
                _name = "P "+str(_dax_desc[0]).upper()+" "+str(_month).upper()+" "+str(_year)+" "+str((start_strike[_temp_num]))
            
            df.loc[i] = [_name,(start_strike[_temp_num]),"DTB",str("OPT").upper()]
            _temp_num+=1
        print(df)
    if asset == "SPX":
        _temp_num = 0
        for i in range(len(start_strike)):
            if option_type == "CALL" or option_type == "call":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"C0"+str((start_strike[_temp_num]))+"000"
            if option_type == "PUT" or option_type == "put":
                _name = "SPXW "+str(_year)+str(_month_num).upper()+str(_day).upper()+"P0"+str((start_strike[_temp_num]))+"000"
            
            df.loc[i] = [_name,(start_strike[_temp_num]),"CBOE",str("OPT").upper()]             
            _temp_num+=1
        print(df)
    if asset == "NG":
        pass
    if asset == "CL":
        _ng_names = [["LO1N2","2022-07-01"],
                     ["LO2N2","2022-07-08"],
                     ["LOQ2","2022-07-15"],
                     ["LO4N2","2022-07-22"],
                     ["LOU2","2022-08-17"],
                     ["LOV2","2022-09-15"],
                     ["LOX2","2022-10-17"],
                     ["LOZ2","2022-11-16"],
                     ["LOF3","2022-12-15"]]

        _date = date_time_obj.strftime('%Y-%m-%d') 
        _desc = [t[0] for t in _ng_names if t[1] == _date ]
        
        _temp_num = 0
        for i in range(len(start_strike)):
            if option_type == "CALL" or option_type == "call":
                _name = str(_desc[0]).upper()+" C"+str((start_strike[_temp_num]*100))
            if option_type == "PUT" or option_type == "put":
                _name = str(_desc[0]).upper()+" P"+str((start_strike[_temp_num]*100))
            
            df.loc[i] = [_name,(start_strike[_temp_num]),"NYMEX",str("OPT").upper()]
            _temp_num+=1
        print(df)
        pass
    if asset == "VIX":
        _names = [["VIXW","2022-06-29"],
                     ["VIXW","2022-07-06"],
                     ["VIXW","2022-07-13"],
                     ["VIX","2022-07-20"],
                     ["VIXW","2022-07-27"],
                     ["VIX","2022-08-17"],
                     ["VIX","2022-09-21"],
                     ["VIX","2022-11-16"],
                     ["VIX","2022-12-21"],
                     ["VIX","2023-01-18"],
                     ["VIX","2023-02-15"],
                     ["VIX","2023-03-22"]]
         
        _date = date_time_obj.strftime('%Y-%m-%d') 
        _desc = [t[0] for t in _names if t[1] == _date ]
        _temp_num = 0
        for i in range(len(start_strike)):
            if option_type == "CALL" or option_type == "call":
                _name = str(_desc[0])+" "+str(_year)+str(_month_num).upper()+str(_day).upper()+"C000"+str((start_strike[_temp_num])*1000)
            if option_type == "PUT" or option_type == "put":
                _name = str(_desc[0])+" "+str(_year)+str(_month_num).upper()+str(_day).upper()+"P000"+str((start_strike[_temp_num])*1000)
            
            df.loc[i] = [_name,(start_strike[_temp_num]),"CBOE",str("OPT").upper()] 
            _temp_num+=1
        print(df)
    if asset == "V2EU":
        _temp_num = 0
        for i in range(len(start_strike)):
            if option_type == "CALL" or option_type == "call":
                _name = "C OVS2 20"+str(_year).upper()+str(_month_num).upper()+str(_day)+" "+str((start_strike[_temp_num]))
            if option_type == "PUT" or option_type == "put":
                _name = "P OVS2 20"+str(_year).upper()+str(_month_num).upper()+" "+str(_day)+" "+str((start_strike[_temp_num]))
            
            df.loc[i] = [_name,(start_strike[_temp_num]),"DTB",str("OPT").upper()] 
            _temp_num+=1
        print(df)
    if asset == "STOXX":
        _temp_num = 0
        for i in range(len(start_strike)):
            if option_type == "CALL" or option_type == "call":
                _name = "C OEXD "+str(_month).upper()+" "+str(_year)+" "+str((start_strike[_temp_num]))
            if option_type == "PUT" or option_type == "put":
                _name = "P OEXD "+str(_month).upper()+" "+str(_year)+" "+str((start_strike[_temp_num]))
            
            df.loc[i] = [_name,(start_strike[_temp_num]),"DTB",str(option_type).upper()]
            _temp_num+=1 
        print(df)
#getSymbols("DAX","2022.09.16",11800,50,"call")
getVecSymbols("DAX","2022.07.01",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("SPX","2022.07.06",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("CL","2022.07.01",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("V2EU","2022.07.06",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("VIX","2022.07.06",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("VIX","2022.07.06",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("VIX","2022.07.06",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("VIX","2022.07.06",[20,25,30,35,40,45,50],0,"call")
getVecSymbols("VIX","2022.07.06",[20,25,30,35,40,45,50],0,"call")


    