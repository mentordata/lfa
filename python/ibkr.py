#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:29:58 2022

@author: Hanna Poplawska for LFA
"""
import pandas as pd
import numpy as np
import sys
from os.path import exists
from datetime import datetime
from pricing import getTradePrice
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Timer
import threading
import time

class TestApp(EWrapper, EClient):

    print("ibkr.py asset timeout buy_offset sell_offset algo")

    if len(sys.argv)!=6:
        print("Inproper arguments")
        sys.exit(-1);


    asset=sys.argv[1];#"dax";
 #   asset="eu50";
    
    timeout=int(sys.argv[2]);        #5*60;        # how many seconds trading will work
    buy_offset=int(sys.argv[3]);     #;      # how many steps price is offset related calculated. >0 helps, lower profit. <0 increase profit
    sell_offset=int(sys.argv[4]);    #   -1;     # how many steps price is offset related calculated. <0 helps, lower profit. >0 increase profit
    algo=sys.argv[5];
    
    profit_sum=0.0;
    profit_count=0;
    
    startSide="BUY";
    endSide="SELL";
    debug=False;
    done = False;
    
#    currentState="OPEN";    #CLOSE
#    currentSide="BUY";
    lock=False;
    
    tdf=pd.DataFrame(pd.read_csv('./'+asset+'_symbols.csv'))
    tdf.at[:,"current_state"]="OPEN";
    tdf.at[:,"current_side"]="BUY";
    
    tdf.at[:,"last_bid"]=0;
    tdf.at[:,"last_ask"]=0;
    tdf.at[:,"a0"]=0.0;
    tdf.at[:,"b0"]=0.0;
    tdf.at[:,"a1"]=0.0;
    tdf.at[:,"b1"]=0.0;
    tdf.at[:,"a2"]=0.0;
    tdf.at[:,"b2"]=0.0;
    tdf.at[:,"a3"]=0.0;
    tdf.at[:,"b3"]=0.0;
    tdf.at[:,"a4"]=0.0;
    tdf.at[:,"b4"]=0.0;
    tdf.at[:,"bid_mean"]=0.0;
    tdf.at[:,"ask_mean"]=0.0;
    
    
#status,price,id_order,bid,ask
    tdf.at[:,"bid"]=0;
    tdf.at[:,"ask"]=0;
    tdf.at[:,"bids"]=0;
    tdf.at[:,"asks"]=0;
    tdf.at[:,"id_order_open"]=-1;
    tdf.at[:,"id_order_close"]=-1;
    tdf.at[:,"profit_inc"]=-1;
    tdf.at[:,"price_open"]=-1;
    tdf.at[:,"price_close"]=-1;
    tdf.at[:,"state"]="FIRST";       #FIRST - wait for open, WAIT - doesnt allow changes, ACTIVE - changes active
    
    
    tdf.at[:,"status_open"]="none";
    tdf.at[:,"status_close"]="none";

    tdf.at[:,"result_sum"]=0.0;
    tdf.at[:,"result_count"]=0;
    

    qp=pd.DataFrame(columns=["timestamp","bid", "ask", "bid2","ask2"])
    
    

    df=tdf.astype({"bids":object, "asks":object, "bid":float, "trade":bool, "ask":float,"id_order_open":int,"id_order_close":int, "price_close":float, "price_open":float,  "status_open":str,"status_close":str, "last_bid":float, "last_ask":float, "step":float})

    for index,x in df.iterrows():
        df.at[index,"bids"]=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0];
        df.at[index,"asks"]=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0];
        

    
#    idSymbol=df[df.loc[:,"trade"]==True].index[0];  # which symbol to trade
    price_step=df.step[0];
        
    pos=pd.DataFrame({"id","fill_price","status_open"})
    
    profit_df=pd.DataFrame(columns={"timestamp","symbol","profit"})

    
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId , errorCode, errorString):
        print(datetime.now(),"Error: reqId:", reqId, " errorCode:", errorCode, " msg: ", errorString)

    def nextValidId(self, orderId ):
        self.nextOrderId = orderId
        self.start()

    def pushOrder(self,reqId,orderId, price, side):
            drow=self.df.iloc[reqId];
            
            contract = Contract();
            contract.localSymbol = drow.symbol;
            contract.secType = drow.type;
            contract.exchange = drow.exchange;
    
            order = Order();
            order.action = side;
            order.totalQuantity = 1;
            order.orderType = "LMT";
            order.lmtPrice = price;

            if orderId<0:            # it is a new order
                orderId=self.nextOrderId;
                self.nextValidId(self.nextOrderId+1);
#                print(datetime.now(),">>> new orderId:",orderId, side, drow.symbol, "@",price);

            order.orderRef="id_"+str(orderId);
            
            if self.lock==False:
                self.placeOrder(orderId, contract, order);
                
            return orderId;



    def orderStatus(self, orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):

        
#        print(datetime.now(),"orderId:",orderId," status:",status)
#        print(datetime.now(),"###",orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice);
        
                 
        idx=-1;
        
        if len(self.df[self.df.loc[:,"id_order_open"]==orderId])>0:
            idx_open=self.df[self.df.loc[:,"id_order_open"]==orderId].index[0];
            idx=idx_open;
            if self.df.at[idx_open,"status_open"]=="Filled":
                return;
            else:
                self.df.at[idx_open,"status_open"]=status;          
            
        if len(self.df[self.df.loc[:,"id_order_close"]==orderId])>0:
            idx_close=self.df[self.df.loc[:,"id_order_close"]==orderId].index[0];
            idx=idx_close;
            if self.df.at[idx_close,"status_close"]=="Filled":
                return;
            else:
                self.df.at[idx_close,"status_close"]=status;          
                    
              
        if status=="Filled" and idx != -1:

            if self.lock==False:
                self.lock=True;     # critical section
    
#                print(datetime.now(),"OrderStatus. Id:", orderId, " Status:", status, " Filled:", filled, " FillPrice:", lastFillPrice)
                
                #switch to closure
                if self.df.at[idx,"current_state"]=="OPEN" and self.df.at[idx,"id_order_open"] == orderId:
#                    print("## id_order_open=",self.df.at[idSymbol,"id_order_open"],orderId);
#                    last_state=self.df.at[idx,"current_state"];
#                    print(self.df.iloc[idSymbol]);
                    self.df.at[idx,"current_state"]="TOCLOSE";
                    self.df.at[idx,"current_side"]="SELL";
                    self.df.at[idx,"id_order_open"]=-1;
                    self.df.at[idx,"status_close"]="none";
#                    print(datetime.now(),"change state from",last_state, "to",self.df.at[idx,"current_state"]);
    
                if self.df.at[idx,"current_state"]=="CLOSE" and self.df.at[idx,"id_order_close"] == orderId:
#                    print("## id_order_close=",self.df.at[idSymbol,"id_order_close"],orderId);
#                   last_state=self.df.at[idx,"current_state"];
#                    print(self.df.iloc[idSymbol]);
                    profit=self.df.at[idx,"price_close"] - self.df.at[idx,"price_open"];
                    self.df.at[idx,"current_state"]="TOOPEN";
                    self.df.at[idx,"current_side"]="BUY";
                    self.df.at[idx,"id_order_open"]=-1;
                    self.df.at[idx,"id_order_close"]=-1;
                    self.df.at[idx,"status_open"]="none";
                    self.df.at[idx,"status_close"]="none";
                    self.df.at[idx,"price_open"]=-1;
                    self.df.at[idx,"price_close"]=-1;
                    self.profit_df=self.profit_df.append({"timestamp":datetime.now(),"symbol":self.df.at[idx,"symbol"],"profit":round(profit,2)}, ignore_index=True);
                    self.df.at[idx,"result_sum"]=self.df.at[idx,"result_sum"]+profit;
                    self.df.at[idx,"result_count"]=self.df.at[idx,"result_count"]+1;
                    print(datetime.now(),"RESULT=",round(profit,2),"from trade on", self.df.at[idx,"symbol"]);
                    
#                    self.stop();
                    
                if self.df.at[idx,"current_state"]=="TOCLOSE":
                    self.df.at[idx,"current_state"]="CLOSE";
#                    print(".. CLOSE");
                    
                if self.df.at[idx,"current_state"]=="TOOPEN":
                    self.df.at[idx,"current_state"]="OPEN";
#                    print(".. OPEN");

                self.lock=False;        # end of critical section

                

    def openOrder(self, orderId, contract, order, orderState):
        exld_list=["Submitted","PendingSubmit","PreSubmitted"];
        if orderState.status not in exld_list:
            if self.debug:
                print(datetime.now(),"OpenOrder. ID:", orderId, order.action, contract.localSymbol, order.orderType, order.totalQuantity,"@",order.lmtPrice, orderState.status)
#        print("orderId:",orderId," status:",orderState.status);
#        
#        if len(self.df[self.df.loc[:,"id_order_open"]==orderId])>0:
#            idx_open=self.df[self.df.loc[:,"id_order_open"]==orderId].index[0];
#            self.df.at[idx_open,"status_open"]=orderState.status;          
#            
#        if len(self.df[self.df.loc[:,"id_order_close"]==orderId])>0:
#            idx_close=self.df[self.df.loc[:,"id_order_close"]==orderId].index[0];
#            self.df.at[idx_close,"status_close"]=orderState.status;          

        
    def execDetails(self, reqId, contract, execution):
#        print(datetime.now(),"ExecDetails. ", reqId, execution.orderId)
        test=1;
        test=test*2;
    

    def start(self):

        test=1;
        test=test*2;
        
#        self.placeOrder(self.nextOrderId, contract, order)
        
    
    def getPrice(self):
        contract = Contract();
# reading symbols from file and request its prices
        df=self.df;
        
        for index,x in df.iterrows():
            contract.localSymbol=x["symbol"];
            contract.secType = x["type"];
            contract.exchange= x["exchange"];
            self.reqMktData(index, contract, "106", False,False, []);
            print("requested for price of",contract.localSymbol,"reqId:",index);
            
        
 
           
        
        
    def tickPrice(self, reqId: int, tickType: int, price: float, attrib: int):
        super().tickGeneric(reqId, tickType, price)
#        print("TickGeneric. TickerId:", reqId, "TickType:", tickType, "Value:", price)
   
   
#        df=self.df;
#        price_step=self.df.loc[0].step;
        
        mean_scope=5
        
        #BID
        if tickType==1:
            self.df.at[reqId,"bids"].insert(0,price);
            self.df.at[reqId,"bids"].pop();
            self.df.at[reqId,"bid_mean"]=round((round(np.mean(self.df.iloc[reqId].bids[0:mean_scope])/self.price_step,0))*self.price_step,2);
#            print("mean:",self.df.at[reqId,"symbol"],"bids:",self.df.iloc[reqId].bids[0:mean_scope])
            
            self.df.at[reqId,"bid"]=price;
            
        #ASK
        if tickType==2:
            
            self.df.at[reqId,"asks"].insert(0,price);
            self.df.at[reqId,"asks"].pop();
            self.df.at[reqId,"ask_mean"]=round((round(np.mean(self.df.iloc[reqId].asks[0:mean_scope])/self.price_step,0))*self.price_step,2);

#            print("mean:",self.df.at[reqId,"symbol"],"asks:",self.df.iloc[reqId].asks[0:mean_scope])
            self.df.at[reqId,"ask"]=price;
       
            
        if (tickType==1 or tickType==2):
####################################################################################        
            pass;
#            if reqId in (0,7):
#                self.qp=self.qp.append({"timestamp":datetime.now(),"bid":self.df.at[0,"bid"],"bid2":self.df.at[1,"bid"],"ask":self.df.at[0,"ask"],"ask2":self.df.at[1,"ask"]},ignore_index=True);
            
#            for idSymbol in self.df[self.df["trade"]].index:
##                self.pdf=self.pdf.append({"timestamp":datetime.now(),"bid":self.df.at[0,"bid"]},ignore_index=True);
##                print(":: trade for idSymbol:",idSymbol);
#                price=-1;
#               
#                if self.df.at[idSymbol,"current_state"]=="OPEN" and self.df.at[idSymbol,"current_side"]=="BUY":
#                    price=getTradePrice(self,idSymbol,self.algo,"BUY");
#    
#                    if self.df.at[idSymbol,"price_open"] != price and price != -1:      #check if price is different than opened
#                        if (self.df.at[idSymbol,"status_open"]=="Submitted") or (self.df.at[idSymbol,"id_order_open"]==-1) :
#                            if self.lock==False:
#                                # if (submitted) or (not opended yet)
#                                orderId=self.pushOrder(idSymbol, self.df.at[idSymbol,"id_order_open"], price, self.df.at[idSymbol,"current_side"]);
#                                self.df.at[idSymbol,"price_open"] = price;
#                                self.df.at[idSymbol,"id_order_open"]=orderId;
#    
#                if self.df.at[idSymbol,"current_state"]=="CLOSE" and self.df.at[idSymbol,"current_side"]=="SELL":
#                    price=getTradePrice(self,idSymbol,self.algo,"SELL");
#    
#                    if self.df.at[idSymbol,"price_close"] != price and price != -1:      #check if price is different than opened
#                        if (self.df.at[idSymbol,"status_close"]=="Submitted") or (self.df.at[idSymbol,"id_order_close"]==-1) :
#                            # if (submitted) or (not opended yet)
#                            if self.lock==False:
#                                orderId=self.pushOrder(idSymbol, self.df.at[idSymbol,"id_order_close"], price, self.df.at[idSymbol,"current_side"]);
#                                self.df.at[idSymbol,"price_close"] = price;
#                                self.df.at[idSymbol,"id_order_close"]=orderId;

####################################################################################                    
            

   
    def tickOptionComputation(self, reqId: int, tickType: int, tickAttrib: int,
                                  impliedVol: float, delta: float, optPrice: float, pvDividend: float,
                                  gamma: float, vega: float, theta: float, undPrice: float):
            super().tickOptionComputation(reqId, tickType, tickAttrib, impliedVol, delta,
                                          optPrice, pvDividend, gamma, vega, theta, undPrice)
            
#            print("TickOptionComputation. TickerId:", reqId, "TickType:", tickType,
#                  "TickAttrib:", tickAttrib,
#                  "ImpliedVolatility:", impliedVol, "Delta:", delta, "OptionPrice:",
#                  optPrice, "pvDividend:", pvDividend, "Gamma: ", gamma, "Vega:", vega,
#                  "Theta:", theta, "UnderlyingPrice:", undPrice)
    
    def stop(self):
        self.done = True
        self.disconnect()
        
        print("===================");
        print(datetime.now());
        print("algo=",self.algo,"timeout=",self.timeout,"buy_offset=",self.buy_offset,"sell_offset=",self.sell_offset);        
        print(self.df);
        print("==========");
        print(self.profit_df);
        print("sharpee=",round(np.mean(self.profit_df.profit)/np.std(self.profit_df.profit),2),"mean=",np.mean(self.profit_df.profit), "count=",len(self.profit_df.profit));
        
        
#        print(self.qp);
        self.qp.to_csv("qp."+self.asset+".csv");
        

        
    def check_if_stop(self):
        if exists("py_stop"):
            self.done = True;
            self.disconnect();
            
    def get_ticks(self):

        print("ticks collection started");
        while self.done==False :
            time.sleep(1);
            print("ticket at ", datetime.now());
            self.qp=self.qp.append({"timestamp":datetime.now(), 
            "bid":self.df.at[0,"bid"], 
            "bid2":self.df.at[1,"bid"], 
            "bid3":self.df.at[2,"bid"], 
            "bid4":self.df.at[3,"bid"], 
            "ask":self.df.at[0,"ask"], 
            "ask2":self.df.at[1,"ask"], 
            "ask3":self.df.at[2,"ask"], 
            "ask4":self.df.at[3,"ask"]},
            ignore_index=True);
        print("ticks collection stopped");
        

def main():
    
    app = TestApp()
    
    app.nextOrderId = 0
    app.connect("127.0.0.1", 7496, 1)
    app.getPrice()
    print("trading started ...");
    
    t1 = threading.Thread(target=app.get_ticks);
    t1.start();
    
    
    Timer(app.timeout, app.stop).start()
    app.run()
    
    
    

        

if __name__ == "__main__":
    main()
