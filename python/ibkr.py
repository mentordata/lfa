#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:29:58 2022

@author: esmx
"""
import pandas as pd
from os.path import exists
from datetime import datetime

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Timer

class TestApp(EWrapper, EClient):

     
    asset="dax";
    
    timeout=5*60;        # how many seconds trading will work
    buy_offset=1;      # how many steps price is offset related calculated. >0 helps, lower profit. <0 increase profit
    sell_offset=-1;     # how many steps price is offset related calculated. <0 helps, lower profit. >0 increase profit
    profit_sum=0.0;
    profit_count=0;
    profit_df=pd.DataFrame();
    
    startSide="BUY";
    endSide="SELL";
    debug=False;
    
#    currentState="OPEN";    #CLOSE
#    currentSide="BUY";
    lock=False;
    
    tdf=pd.DataFrame(pd.read_csv('/home/esmx/.config/spyder-py3/'+asset+'_symbols.csv'))
    tdf.at[:,"current_state"]="OPEN";
    tdf.at[:,"current_side"]="BUY";
    
    tdf.at[:,"last_bid"]=0;
    tdf.at[:,"last_ask"]=0;
#status,price,id_order,bid,ask
    tdf.at[:,"bid"]=0;
    tdf.at[:,"ask"]=0;
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
    
    
    

    df=tdf.astype({"bid":float, "trade":bool, "ask":float,"id_order_open":int,"id_order_close":int, "price_close":float, "price_open":float,  "status_open":str,"status_close":str, "last_bid":float, "last_ask":float, "step":float})
    
    idSymbol=df[df.loc[:,"trade"]==True].index[0];  # which symbol to trade
    
        
    pos=pd.DataFrame({"id","fill_price","status_open"})

    
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
#                    self.profit_df=round(self.profit_df.append({"result":profit}, ignore_index=True),2);
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
            print("requested for price of",contract.localSymbol);
            
        
 
           
        
        
    def tickPrice(self, reqId: int, tickType: int, price: float, attrib: int):
        super().tickGeneric(reqId, tickType, price)
#        print("TickGeneric. TickerId:", reqId, "TickType:", tickType, "Value:", price)
   
   
#        df=self.df;
        price_step=self.df.loc[0].step;
        
        #BID
        if tickType==1:
            self.df.at[reqId,"last_bid"]=self.df.at[reqId,"bid"];
            self.df.at[reqId,"bid"]=price;
            
        #ASK
        if tickType==2:
            self.df.at[reqId,"last_ask"]=self.df.at[reqId,"ask"];
            self.df.at[reqId,"ask"]=price;
       
#            ask=self.df.at[reqId,"ask"];
#            bid=self.df.at[reqId,"bid"];
            
   
#            if prices_ok == False:
#        print("bid/ask:",bid_a,' ',ask_a," ",bid_b, " ",ask_b ,"(",price,")");
            
        if (tickType==1 or tickType==2):
####################################################################################        

            for idSymbol in self.df[self.df["trade"]].index:
#                print(":: trade for idSymbol:",idSymbol);
                price=-1;
                
                ask_a=self.df.at[idSymbol-1,"ask"];
                bid_a=self.df.at[idSymbol-1,"bid"];
                ask_b=self.df.at[idSymbol+1,"ask"];
                bid_b=self.df.at[idSymbol+1,"bid"];
        
                # check if data are ok
                prices_ok=(ask_a>0) and (ask_b>0) and (bid_a>0) and (bid_b>0);

                if prices_ok: 
               
                    if self.df.at[idSymbol,"current_state"]=="OPEN" and self.df.at[idSymbol,"current_side"]=="BUY":
                        price=round((round(((bid_a+ask_b)/2)/price_step,0)+self.buy_offset)*price_step,2);
        
                        if self.df.at[idSymbol,"price_open"] != price:      #check if price is different than opened
                            if (self.df.at[idSymbol,"status_open"]=="Submitted") or (self.df.at[idSymbol,"id_order_open"]==-1) :
                                if self.lock==False:
                                    # if (submitted) or (not opended yet)
                                    orderId=self.pushOrder(idSymbol, self.df.at[idSymbol,"id_order_open"], price, self.df.at[idSymbol,"current_side"]);
                                    self.df.at[idSymbol,"price_open"] = price;
                                    self.df.at[idSymbol,"id_order_open"]=orderId;
        
                    if self.df.at[idSymbol,"current_state"]=="CLOSE" and self.df.at[idSymbol,"current_side"]=="SELL":
                        price=round((round(((bid_b+ask_a)/2)/price_step,0)+self.sell_offset)*price_step,2);
        
                        if self.df.at[idSymbol,"price_close"] != price:      #check if price is different than opened
                            if (self.df.at[idSymbol,"status_close"]=="Submitted") or (self.df.at[idSymbol,"id_order_close"]==-1) :
                                # if (submitted) or (not opended yet)
                                if self.lock==False:
                                    orderId=self.pushOrder(idSymbol, self.df.at[idSymbol,"id_order_close"], price, self.df.at[idSymbol,"current_side"]);
                                    self.df.at[idSymbol,"price_close"] = price;
                                    self.df.at[idSymbol,"id_order_close"]=orderId;

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
        print("timeout=",self.timeout,"buy_offset=",self.buy_offset,"sell_offset=",self.sell_offset);        
        print(self.df);
        print("sum=",sum(self.df.result_sum));

        
    def check_if_stop(self):
        if exists("py_stop"):
            self.done = True;
            self.disconnect();

def main():
    
    app = TestApp()
    
    app.nextOrderId = 0
    app.connect("127.0.0.1", 7497, 1)
    app.getPrice()
    print("trading started ...");
    
    
    Timer(app.timeout, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()