from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile, asksaveasfile
from PIL import Image, ImageTk
import os
import pandas as pd
import pyodbc
import numpy as np
import math

MAX_WIDTH = 800
MAX_HEIGHT = 600



def convert(text):
    try:
        return int(text)
    except ValueError:
        pass

    try:
        return float(text)
    except ValueError:
        return text



class MyGUI:
    def __init__(self,root):
        self.root = root;
        root.title("LFA | Send data to database")

        #======================DATABASE CONNECTION===========================

        
        #Specifying the ODBC driver, server name, database, etc. directly
        self.cnxn = pyodbc.connect('DRIVER={IBM DB2 ODBC DRIVER - IBMDBCL1};SERVER=localhost;DATABASE=lfa00;UID=;PWD=') # UID and PWD not provided
        self.cursor = self.cnxn.cursor()
        #=========================F R A M E S================================

        self.content = Frame(self.root, padx=3,pady=12)
        self.frame = Frame(self.content, borderwidth=5, relief="ridge", width=300, height=400)
        self.main_box = Frame(self.content, borderwidth=5, relief="ridge", width=300, height=200)

        #-------------------------OTHER LABELS-----------------------------
        
        self.steps = StringVar()
        self.steps.set('1. Connect to database via ssh tunnel (to dev.mentordata.com) \n2. Choose file .xls or .xlsx \n3. Click "Send to database" button')
        self.steps_msg = ttk.Label(self.frame,textvariable=self.steps,wraplength=300,justify="left")


        self.response = StringVar()
        self.response.set('PLEASE REMEMBER ABOUT CREATING CONNECTION WITH REMOTE DATABASE VIA "git bash" BEFORE SENDING FILE!')
        self.info_msg = ttk.Label(self.frame,textvariable=self.response,wraplength=200,justify="center")

        #-----------------F R A M E   B U T T O N S------------------------
        

        #--------------------F R A M E   G R I D---------------------------
        
        self.steps_msg.grid(column=0,row=0,columnspan=2)
        ttk.Separator(self.frame,orient=HORIZONTAL).grid(column=0,row=1,columnspan=2,sticky='we')

        ttk.Separator(self.frame,orient=HORIZONTAL).grid(column=0,row=5,columnspan=2,sticky='we')

        self.info_msg.grid(column=0,row=6,columnspan=6)

        #==========================MAIN BOX=================================

        self.path_name = StringVar()
        self.path_name.set("Choose a file...")
        self.path_box = Entry(self.main_box,textvariable=self.path_name,width=100)

        self.browse_text = StringVar()
        self.browse_btn = ttk.Button(self.main_box,textvariable=self.browse_text,command=lambda:self.open_file())
        self.browse_text.set("Browse")

        self.send = StringVar()
        self.send_btn = ttk.Button(self.main_box,textvariable=self.send,command=lambda:self.send_file())
        self.send.set("Send to database")
        
        self.update = StringVar()
        self.update_btn = ttk.Button(self.main_box,textvariable=self.update,command=lambda:[self.delete_file(),self.send_file()])
        self.update.set("Update file in database")
        

        self.path_box.grid(column=0,row=0)
        self.browse_btn.grid(column=0,row=1)
        self.send_btn.grid(column=0,row=2)
        self.update_btn.grid(column=0,row=3)

        #======================GRID WIDGET REPOSITION=======================

        self.content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self.main_box.grid(column=3, row=0, columnspan=2, sticky=(N, S, E, W), padx=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=3)
        self.content.columnconfigure(1, weight=3)
        self.content.columnconfigure(2, weight=3)
        self.content.columnconfigure(3, weight=1)
        self.content.columnconfigure(4, weight=1)
        self.content.rowconfigure(1, weight=1)


    def open_file(self):
            file = askopenfile(parent=root,mode='rb',title="Choose a file",filetype=[("Excel file","*.xls *.xlsx")])
            self.path_name.set(file.name)
    
    def delete_file(self):

        f = (open(self.path_box.get(),"rb"))
        read_file = pd.read_excel(self.path_box.get())

        base = os.path.basename(self.path_box.get())
        filename = os.path.splitext(base)[0]

        drop = "DROP TABLE {}".format('temp_'+filename)

        # Delete Table
        print("DELETING TABLE...")
        self.cursor.execute(drop)
        self.cursor.commit()
        

    def send_file(self):
        f = (open(self.path_box.get(),"rb"))
        read_file = pd.read_excel(self.path_box.get())

        base = os.path.basename(self.path_box.get())
        filename = os.path.splitext(base)[0]

        read_file.to_csv(filename+".csv", index=False,
                header = True)
        data = pd.read_csv (filename+'.csv',na_filter=False)
        data = data.applymap(str)
        #data = data.apply(pd.to_numeric,errors='ignore')
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
        #data = data.replace(np.nan,'-',regex=True)

        list_of_column_names = list(read_file.columns)
        #print('List of column names: ',list_of_column_names)
        list_of_types = list(data.dtypes)
        #print("DATA TYPES IN COLUMNS: \n ",list_of_types)
        types = ' '.join([str(v) for v in list_of_types])
        types = list(types.split(" "))
        print("DATA TYPES IN COLUMNS: \n ",types)
        types = ["VARCHAR" if x == 'object' else x for x in types]
        types = ["INTEGER" if x == 'int64' else x for x in types]
        types = ["DECFLOAT" if x == 'float64' else x for x in types]
        types = ["DATE" if x == 'datetime64[ns]' else x for x in types]

        measurer = np.vectorize(len)
        res1 = measurer(data.values.astype(str)).max(axis=0)
        print(res1)
        max1 = [int(math.ceil(x/10))*10 for x in res1]
        #print("MAX FOR EACH COLUMN",max1)
        #print(types)
        

        column_list = list(zip(list_of_column_names,types,max1))
        print(column_list)

        # CREATING QUERY TO CREATE CUSTOM TABLE
        
        sql = "CREATE TABLE {0}(".format('temp_'+filename)
        for x in column_list:
            if x[1] == "VARCHAR":
                sql+="{0} {1}({2}),".format(x[0],x[1],x[2])
            if x[1] == "INTEGER":
                sql+="{0} {1},".format(x[0],x[1])
            if x[1] == "DECFLOAT":
                sql+="{0} {1},".format(x[0],x[1])
            if x[1] == "DATE":
                sql+="{0} {1},".format(x[0],x[1])
        sql+=")"
        query = sql[:-2]+sql[-1:]
        print("SQL QUERY: ",query)

        insert = "INSERT INTO {}(".format('temp_'+filename)+', '.join(list_of_column_names)+") VALUES("+', '.join(['?' for _ in range(len(list_of_column_names))])+')'
        print("INSERT QUERY: ",insert)
        # Create Table
        print("CREATING TABLE...")
        self.cursor.execute(query)
        self.cursor.commit()
        
        # Insert to table
        self.cursor.fast_executemany = True
        df_records = data.values.tolist()
        print("INSERTING DATA...")
        self.cursor.executemany(insert,df_records)
        self.cursor.commit()
        
        self.response.set("STATUS: Data has been uploaded. Created table and inserted data. If you want to continue, please choose another excel file.")
        print("STATUS: Data has been uploaded. Created table and inserted data. If you want to continue, please choose another excel file.")

        


#=========================TKINTER==================================
root = Tk()
my_gui = MyGUI(root)

root.mainloop()

