import pdfplumber
import pandas as pd
from pprint import pprint
import datetime
import re
import sys
import os
import traceback
import sqlite3
import csv

# result file:
resultFile = open("resultFile.txt", 'w',encoding='utf-8')
#resultFile.write("data,godzina,numer,siec,typ,numer_przychodzacy,liczba,dozaplaty\n")
resultFile.write("date,time,number,host,type,network,period\n")
# database
database_name = sys.argv[2] + ".db"
table_name = sys.argv[3]
con = sqlite3.connect(database_name)
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS "+str(table_name))
cur.execute("CREATE TABLE "+str(table_name)+" (date date, time time, number varchar(20), host varchar(20), type varchar(20), network varchar(20), period number)")


for filename in os.listdir(sys.argv[1]):
    f = os.path.join(sys.argv[1], filename)
    if filename.endswith('.pdf'):
        pass
    else:
        print("[ERROR] Found unsupported file (not .pdf): ",f)
        continue

    text = ""

    # GLOBAL VARIABLES
    current_number = 0


    #TEMP VAR
    counter = 1
    temp_file_list = []

    # READING DATA FROM PDF AND PUTTING PER PAGE INTO TEMP_PAGE_TEXT
    with pdfplumber.open(f) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            filename = "temp_file_"+str(counter)+".txt"
            #print(filename)
            temp_file_list.append(filename)
            #print(temp_file_list)
            with open(filename,"w",encoding='utf-8') as temp:
                temp.write(text)
            temp.close()
            counter+=1

    final_list = []
    client_number = []
    print("[INFO] Started processing file: ",f)
    try:
        for temp_n in temp_file_list:
            temp = open(temp_n,"r",encoding='utf-8')
            lines = temp.readlines()

            good_row = []

            first_list = []
            sec_list = []

            items_to_remove = ['ˬʔ','ˬ','˛','˛ƺ','˛ʔ']

            counter_r = 0
            for line in lines:
                line.strip()
                line_parts = line.split()
                if (len(line_parts)>=9 and re.search('brutto za telefon',line.strip())):
                    number = re.search(r'za telefon nr (.*)',line.strip()).group(1)
                    client_number.append(int(number[0:9]))
            #print(client_number)
            for row in lines:
                row.strip()
                row_parts = row.split()

                #print(row_parts)
                # deleting unnecessary ASCII characters
                for i in range(2):
                    for item in items_to_remove:
                        if item in row_parts:
                            row_parts.remove(item)
                #print(row_parts)
                days = ["Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota","Niedziela"]

                if(len(row_parts) == 2 or len(row_parts) == 4):
                    if row_parts[1] in days:
                        row_parts[0] = row_parts[0].replace(",","")
                        good_row.append(row_parts)
                #if(len(row_parts) == 4 and row_parts[0][2].isnumeric() and row_parts[0][4] == '.') or (len(row_parts) == 4 and row_parts[0][1].isnumeric() and row_parts[0][3] == '.'):
                #    row_parts[0] = row_parts[0].replace(",","")
                    #print(row_parts)
                #    good_row.append(row_parts)
                if(len(row_parts) == 7 or len(row_parts) == 8):
                    if (row_parts[2].isnumeric() or row_parts[3].isnumeric()) and row_parts[0][2]==':':
                        good_row.append(row_parts)
                       
                if(len(row_parts) >= 9 and ((row_parts[2].isdigit() and len(row_parts[2]) == 9 ) or (row_parts[3].isdigit() and len(row_parts[3]) == 9 ) or (row_parts[4].isdigit()  and len(row_parts[4]) == 9) or (row_parts[5].isdigit() and len(row_parts[5]) == 9)) and row_parts[3] != 'internet'):
                    row_parts[0] = row_parts[0].replace(",","")
                    #print(row_parts)
                    good_row.append(row_parts)
                    
                        

            fix_list = []

            prev_date = datetime.date(2000,1,1)


            for row in good_row:
                #print(row)
                #print(len(row))

                # getting date
                if len(row[0]) == 10:
                    if row[0][2] != '.':
                        __date = datetime.datetime.strptime(row[0],'%Y.%m.%d').date()
                    else:
                        __date = datetime.datetime.strptime(row[0],'%d.%m.%Y').date()

                #print(__date)

                if __date >= prev_date:
                    prev_date = __date
                else:
                    fix_list.append(row)
                    continue


                # creating proper data lists
                
                if(len(row) == 2 or len(row) == 7 or len(row) == 8):
                    first_list.append(row)
                
                if(len(row) == 14 or len(row) == 15 or len(row) == 16):
                    # [DATA][DATA]
                    if (len(row[2]) == 9 or len(row[3]) == 9 ) and (len(row[10]) == 9 or len(row[11]) == 9 ):
                        row[0] = row[0].replace(",","")
                        if (len(row[2])== 9 and row[2].isnumeric()):
                            first_list.append(row[:7])
                            sec_list.append(row[7:])
                        else:
                            first_list.append(row[:8])
                            sec_list.append(row[8:])
                        #print("FIRST_LIST: ",first_list)
                        #print("SEC_LIST",sec_list)
                if(len(row) == 4):
                    # [DATE][DATE]
                    #if (row[0][4] == '.' and row[2][2] == ':') or (row[0][2] == '.' and row[2][2] == ':'):
                        row[0] = row[0].replace(",","")
                        row[2] = row[2].replace(",","")
                        first_list.append(row[:2])
                        sec_list.append(row[2:])
                        #print("FIRST_LIST: ",first_list)
                        #print("SEC_LIST",sec_list)
                if(len(row) == 9 or len(row) == 10):
                    # [DATE][DATA]
                    if (row[0][4] == '.' and row[2][2] == ':') or (row[0][2] == '.' and row[2][2] == ':'):
                        row[0] = row[0].replace(",","")
                        first_list.append(row[:2])
                        sec_list.append(row[2:])
                        continue
                    # [DATA][DATE] ------------------- CHECK 
                    else:
                    #if (row[7][4] == '.' or row[8][4] == '.') and (len(row[2]) == 9 or len(row[3]) == 9 ):
                        row[0] = row[0].replace(",","")
                        if (len(row[2]) == 9 and row[2].isnumeric()):
                            first_list.append(row[:7])
                            sec_list.append(row[7:])
                        else:
                            first_list.append(row[:8])
                            sec_list.append(row[8:])

            #pprint(first_list+sec_list)
            for i in first_list:
                final_list.append(i)
            for i in sec_list:
                final_list.append(i)

            first_list = []
            sec_list = []

            if fix_list:
                for row in fix_list:
                #print(row)
                # creating proper data lists
                
                    if(len(row) == 2 or len(row) == 7 or len(row) == 8):
                        first_list.append(row)
                
                    if(len(row) == 15 or len(row) == 16):
                        # [DATA][DATA]
                        if (len(row[2]) == 9 or len(row[3]) == 9 ) and (len(row[10]) == 9 or len(row[11]) == 9 ):
                            row[0] = row[0].replace(",","")
                            if (len(row[2])== 9 and row[2].isnumeric()):
                                first_list.append(row[:7])
                                sec_list.append(row[7:])
                            else:
                                first_list.append(row[:8])
                                sec_list.append(row[8:])
                            #print("FIRST_LIST: ",first_list)
                            #print("SEC_LIST",sec_list)
                    if(len(row) == 4):
                        # [DATE][DATE]
                        #if (row[0][4] == '.' and row[2][2] == ':') or (row[0][2] == '.' and row[2][2] == ':'):
                            row[0] = row[0].replace(",","")
                            row[2] = row[2].replace(",","")
                            first_list.append(row[:2])
                            sec_list.append(row[2:])
                            #print("FIRST_LIST: ",first_list)
                            #print("SEC_LIST",sec_list)
                    if(len(row) == 9 or len(row) == 10):
                        # [DATE][DATA]
                        if (row[0][4] == '.' and row[2][2] == ':') or (row[0][2] == '.' and row[2][2] == ':'):
                            row[0] = row[0].replace(",","")
                            first_list.append(row[:2])
                            sec_list.append(row[2:])
                            continue
                        # [DATA][DATE] ------------------- CHECK 
                        else:
                        #if (row[7][4] == '.' or row[8][4] == '.') and (len(row[2]) == 9 or len(row[3]) == 9 ):
                            row[0] = row[0].replace(",","")
                            if (len(row[2]) == 9 and row[2].isnumeric()):
                                first_list.append(row[:7])
                                sec_list.append(row[7:])
                            else:
                                first_list.append(row[:8])
                                sec_list.append(row[8:])

                #pprint(first_list+sec_list)
                for i in first_list:
                    final_list.append(i)
                for i in sec_list:
                    final_list.append(i)

            #print("=================================================================================================================")


        #pprint(final_list[0:5])
        #print("=================================================================================================================")
        temp_date = []
        prev_date = datetime.date(2000,1,1)
        curr_date = ""
        typ = ""
        num_changed = 0

        row_counter = 0
        for x in final_list:
            #print(x)
            if len(x) == 2:
                x[0] = x[0].replace(",","")
                x[0] = x[0].replace(" ","")
                temp_date = x
            else:
                if len(x) == 8:
                    x[1:3] = [' '.join(x[1:3])]
                if temp_date[0][2] != '.':
                    _date = datetime.datetime.strptime(temp_date[0],'%Y.%m.%d').date()
                else:
                    _date = datetime.datetime.strptime(temp_date[0],'%d.%m.%Y').date()
                _hour = datetime.datetime.strptime(x[0],'%H:%M').time()
                #print(_date)
                if x[3] == '1':
                    typ = "sms"
                else:
                    typ = "call"
                if(_date >= prev_date):
                    if num_changed == 0:
                        prev_date = _date
                        current_client_number = client_number[0]
                    else:
                        prev_date = _date
                        current_client_number = client_number[1]
                else:
                    current_client_number = client_number[1]
                    prev_date = _date
                    num_changed = 1
                x[1] = x[1].replace(", ","_")
                #print(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+x[1]+","+typ+","+x[2]+","+x[3]+","+x[6].replace(",","."))
                
                #resultFile.write("data,godzina,numer,siec,typ,numer_przychodzacy,liczba,dozaplaty\n")
                #resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+x[1]+","+typ+","+x[2]+","+x[3]+","+x[6].replace(",",".")+"\n")
                
                #resultFile.write("date,time,number,host,type,network,period\n")
                resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+x[2]+","+str(current_client_number)+","+typ+","+x[1]+","+x[3]+"\n")
                row_counter+=1
        #pprint(final_list[0:5])
        #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    except Exception as e:
        print("[ERROR] ",line_parts,traceback.format_exc()," |  occured in file: ",f)

        print("Proceeding to next file...\n")

    print(">>> Processed "+str(row_counter)+" rows.\n")
resultFile.close()

# txt to csv
read_file = pd.read_csv (r'resultFile.txt',encoding="utf-8")
read_file.to_csv (r'resultFile.csv',encoding="utf-8")

# inserting data to database
with open('resultFile.csv','r',encoding="utf-8") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['date'],i['time'],i['number'],i['host'],i['type'],i['network'],i['period']) for i in dr]

cur.executemany("INSERT INTO "+str(sys.argv[3])+"(date,time,number,host,type,network,period) VALUES (?,?,?,?,?,?,?);", to_db)
con.commit()


#res = cur.execute('SELECT * FROM bills LIMIT 10')
#pprint(res.fetchall())
con.close()
