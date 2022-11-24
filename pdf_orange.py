from PyPDF2 import PdfReader
import datetime
import sys

# text preparation - using temp as medium to paste data from pdf and read for prorgam usage

text = ""
tempfile = open("temp.txt", "w")

reader = PdfReader(sys.argv[1])
for page in reader.pages:
    text += page.extract_text() + "\n"
tempfile.write(text)

tempfile.close()

resultFile = open("resultFile.txt", 'w')
resultFile.write("data,godzina,siec,numer,liczba,dozaplaty\n")

file = open("temp.txt", "r")
lines = file.readlines()

file_version = 0

# few helpful functions

def hasNumbers(inputString):
    return any(char.isnumeric() for char in inputString)

def merge_net(lst):
    if(lst[2].isdigit() and len(lst[2]) == 9):
        lst[0:2] = [' '.join(lst[0:2])]


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

temp_list = []
if(file_version == 1):
    for line in lines:
        line.strip()
        line_parts = line.split()

        if(len(line_parts) == 2 and '.' in line_parts[0] and line_parts[0][0].isdigit()):
            _date = datetime.datetime.strptime(str(line_parts[0][:-1]), '%d.%m.%Y').date()
        if(len(line_parts) == 8 or len(line_parts) == 9):
            _hour = datetime.datetime.strptime(str(line_parts[0]), '%H:%M').time()

            if(len(line_parts[3])==9):
                _network = line_parts[2]
            else:
                _network = line_parts[2]+" "+line_parts[3]

            if(line_parts[-4] != '1'):
                resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+_network+","+line_parts[-5]+","+line_parts[-4]+","+line_parts[-1].replace(",",".")+"\n")
              
else:
    for line in lines:
        line.strip()
        line_parts = line.split()

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
                        resultFile.write(_date.isoformat()+","+_hour.isoformat()+","+_network+","+x[4]+","+x[5]+","+x[-1].replace(",",".")+"\n")


file.close()
resultFile.close()
