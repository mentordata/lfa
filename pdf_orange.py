from PyPDF2 import PdfReader
import datetime
import sys
import os
import re

# few helpful functions

def hasNumbers(inputString):
    return any(char.isnumeric() for char in inputString)

def merge_net(lst):
    if(lst[2].isdigit() and len(lst[2]) == 9):
        lst[0:2] = [' '.join(lst[0:2])]

# loop through given directory

resultFile = open("resultFile.txt", 'w')
resultFile.write("data,godzina,numer,siec,typ,numer_przychodzacy,liczba,dozaplaty\n")

for filename in os.listdir(sys.argv[1]):
    f = os.path.join(sys.argv[1], filename)
    if filename.endswith('.pdf'):
        pass
    else:
        print("[ERROR] Found unsupported file (not .pdf): ",f)
        continue

    # text preparation - using temp as medium to paste data from pdf and read for prorgam usage
    
    
    text = ""
    tempfile = open("temp.txt", "w")

    reader = PdfReader(f,strict=False)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    tempfile.write(text)

    tempfile.close()

    file = open("temp.txt", "r")
    lines = file.readlines()

    file_version = 0
    current_client_number = 0

    # variables for diagnostics
    row_counter = 0
    ignored_rows = 0
    # diagnostics output
    
    print("[INFO] Started processing file: ",f)

    # checking format of file based on date format

    with open("temp.txt", 'r') as fp:
        lines = fp.readlines()
        for row in lines:
            row.strip()
            row_parts = row.split()
            if(len(row_parts)==8 or len(row_parts)==9):
                if(row_parts[0][2] == ':'):
                    file_version = 1
                else:
                    file_version = 2

    # main part of program
    try:
        temp_list = []
        if(file_version == 1):
            for line in lines:
                line.strip()
                line_parts = line.split()

                if (len(line_parts)>=9 and re.search('brutto za telefon',line.strip())):
                    number = re.search(r'za telefon nr (.*)',line.strip()).group(1)
                    current_client_number = int(number[0:9])
                if(len(line_parts) == 2 and '.' in line_parts[0] and line_parts[0][0].isdigit() and len(line_parts[0])== 11):
                    _date = datetime.datetime.strptime(str(line_parts[0][:-1]), '%d.%m.%Y').date()
                if(len(line_parts) == 6):
                    if(":" in line_parts[0]):
                        _hour = datetime.datetime.strptime(str(line_parts[0][0:5]), '%H:%M').time()
                    else:
                        continue
                    _network = line_parts[0][6:]
                    if(line_parts[-4] != '1'):
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",call,"+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
                        row_counter+=1
                    else:
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",sms,"+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
                        row_counter+=1
                if(len(line_parts) == 7):
                    if(":" in line_parts[0]):
                        _hour = datetime.datetime.strptime(str(line_parts[0][0:5]), '%H:%M').time()
                    else:
                        continue
                    if(len(line_parts[0]) == 7):    #Polska
                        _network = line_parts[1]
                    else:
                        if(line_parts[1] == "mobile"):
                            _network = "nju mobile"
                        if(line_parts[1] == "P4"):
                            _network = "sieć P4"
                        if(line_parts[1] == "Polkomtel"):
                            _network = "sieć Polkomtel"
                        if(line_parts[1] == "T-mobile"):
                            _network = "sieć T-mobile"
                    
                    if(line_parts[-4] != '1'):
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",call,"+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
                        row_counter+=1
                    else:
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",sms,"+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
                        row_counter+=1
                if(len(line_parts) == 8 or len(line_parts) == 9):
                    if("," not in line_parts[-1] or len(line_parts[-5]) != 9):
                        continue
                    _hour = datetime.datetime.strptime(str(line_parts[0][0:5]), '%H:%M').time()

                    if(len(line_parts[3])==9):
                        if(line_parts[2] == "mobile"):
                            _network = "nju mobile"
                        if(line_parts[2] == "P4"):
                            _network = "sieć P4"
                        if(line_parts[2] == "Polkomtel"):
                            _network = "sieć Polkomtel"
                        if(line_parts[2] == "T-mobile"):
                            _network = "sieć T-mobile"
                    else:
                        _network = line_parts[2]+" "+line_parts[3]
                    
                    if(line_parts[-4] != '1'):
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",call,"+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
                        row_counter+=1
                    else:
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",sms,"+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
                        row_counter+=1
        if(file_version == 2):
            for line in lines:
                line.strip()
                line_parts = line.split()

                if (len(line_parts)>=9 and re.search('brutto za telefon',line.strip())):
                    number = re.search(r'za telefon nr (.*)',line.strip()).group(1)
                    current_client_number = int(number[0:9])
                if(len(line_parts) == 1):
                    if(':' in line_parts[0] and hasNumbers(line_parts[0])):
                        if len(temp_list) == 1:
                            temp_list.append(line_parts)
                        if len(temp_list) >= 2:
                            temp_list[1] = line_parts
                if(len(line_parts) == 2):
                    if(len(line_parts) == 2 and '.' in line_parts[0] and line_parts[0][0].isdigit()):
                        if temp_list:
                                temp_list[0] = line_parts
                        else:
                            temp_list.append(line_parts)
                if(len(line_parts) > 2):
                    if(len(line_parts) == 6 or len(line_parts) == 7 or len(line_parts) == 8):
                        if((len(line_parts[1]) == 9 or len(line_parts[2]) == 9 ) and (line_parts[1].isdigit() or line_parts[2].isdigit())):
                            merge_net(line_parts)
                            if len(temp_list) == 2:
                                temp_list.append(line_parts)
                            if len(temp_list) > 2:
                                temp_list[2] = line_parts
                            x = [item for sublist in temp_list for item in sublist]
                            x[0] = x[0].rstrip(',')
                            #print(x)
                            if(x[0][2]=='.'):
                                _date = datetime.datetime.strptime(str(x[0]), '%d.%m.%Y').date()
                            else:
                                _date = datetime.datetime.strptime(str(x[0]), '%Y.%m.%d').date()
                            _hour = datetime.datetime.strptime(str(x[2]), '%H:%M').time()
                            _network = x[3]
                            if(x[5] != '1'):
                                resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",call,"+x[4]+","+x[5]+","+x[-1].replace(",",".")+"\n")
                                row_counter+=1
                            else:
                                resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+str(current_client_number)+","+_network+",sms,"+x[4]+","+x[5]+","+x[-1].replace(",",".")+"\n")
                                row_counter+=1
    except Exception as e:
        print("[ERROR] ",sys.exc_info()[0]," occured in file: ",f)
        
        print("Proceeding to next file...\n")
    print(">>> Processed "+str(row_counter)+" rows.\n")
    
    file.close()
print("Program finished.")
resultFile.close()
