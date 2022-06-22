from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import pandas as pd

import time

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.df = pd.DataFrame(columns=['date','open','bid','ask','close','volume'])

    

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)
        errorCodesG = ["2104","2106","2158"]
        if errorCode not in errorCodesG:
            app.disconnect()
  

    def historicalData(self, reqId, bar):
        # print("HistoricalData. ", reqId, 
        # " Date:", bar.date, 
        # "Open:", bar.open, 
        # "High:", bar.high, 
        # "Low:", bar.low, 
        # "Close:", bar.close, 
        # "Volume:", bar.volume, 
        # "Count:", bar.barCount, 
        # "WAP:", bar.average)
        self.df.loc[len(self.df)] = [bar.date,bar.open,bar.high,bar.low,bar.close,bar.volume]
        

    def historicalDataEnd(self, reqId, start, end):
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)

        self.df.to_csv(str(contract.secType)+"_"+str(contract.symbol)+"_"+str(contract.exchange) + ".csv",index=False,decimal=',')

        app.disconnect() 
        print("Finished")



if __name__ == "__main__":
    
        print("SIMPLE PROGRAM TO DOWNLOAD DATA FROM IBKR USING TWS API. \n")

        print("SETUP CONTRACT: ")

        contract = Contract() 
        # contract.symbol = "CGB"
        # contract.conId = "429253462"
        # contract.exchange = "CDE"
        # contract.secType = "FUT"
        contract.symbol = input("SYMBOL: ")
        contract.conId = input("CONID: ")
        contract.exchange = input("EXCHANGE: ")
        contract.secType = input("secTYPE: ")
        date_period = input("DATE PERIOD: ")
        date_bar = input("BARS: ")
        whattoshow = input("WHAT TO SHOW: ")

        app = TestApp()

        app.connect("127.0.0.1", 7496, 2)

        time.sleep(2)
        app.reqHistoricalData(1, contract, "", date_period, date_bar, whattoshow, 0, 1, False, [])
        time.sleep(5)

        app.run()    
        print("Disconnected.")    

            
     
    
