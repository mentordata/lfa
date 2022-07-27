import sqlite3
import pandas as pd
import ast

# connecting to database
cnx = sqlite3.connect('symbols.db')

df = pd.read_sql_query("SELECT * FROM symbols", cnx)

cnx.commit()
# closing database
cnx.close()

def get_price_step(tab,price):

    if isinstance(tab,str):
        tab = ast.literal_eval(tab)
    if not isinstance(tab,list):
        return "Provided data is not a list type."
    if len(tab) == 0:
        return "List price_func is empty."
    if (len(tab)%2) == 0:
        return "List contains even number of elements"
    if tab[0] == 0:
        return "First element of list is 0."

    if len(tab) == 1:
        return tab[0]
    else:
        step = tab[0]

        idx = 1

        while idx<len(tab) and price>tab[idx]:
            step = tab[idx+1]
            idx = idx+2

        return step

# for testing purposes - uncomment to work
# example: 
#price_list = df["price_inc"][0]
#price = 10
#print("get_price_step: ",get_price_step(price_list,price))



