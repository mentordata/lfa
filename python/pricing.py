#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 11:49:01 2022

@author: Hanna Poplawska for LFA
"""

def getTradePrice(self,idSymbol, algo, side):
    price=-1;   # default one - means that there is no trade oportunity
    
    
    
    if algo=="daino":
        # midpoint between idSymbol-1.bid and idSymbol+1.ask
        ask_a=self.df.at[idSymbol-1,"ask"];
        bid_a=self.df.at[idSymbol-1,"bid"];
        ask_b=self.df.at[idSymbol+1,"ask"];
        bid_b=self.df.at[idSymbol+1,"bid"];

        # check if data are ok
        prices_ok=(ask_a>0) and (ask_b>0) and (bid_a>0) and (bid_b>0);
        
        if prices_ok:
            if side=="BUY":
                price=round((round(((bid_a+ask_b)/2)/self.price_step,0)+self.buy_offset)*self.price_step,2);
            else:
                price=round((round(((bid_b+ask_a)/2)/self.price_step,0)+self.sell_offset)*self.price_step,2);
        else:
            price=-1;

    if algo=="visione":
        # mean reversion trading, buy when ask dropped, close when bid is peaking OR bid+offset > price_open

        ask_x=self.df.at[idSymbol,"ask"];
        bid_x=self.df.at[idSymbol,"bid"];
        ask_mean=self.df.at[idSymbol,"ask_mean"];
        bid_mean=self.df.at[idSymbol,"bid_mean"];
        # check if data are ok
        prices_ok=(self.df.at[idSymbol,"b4"]>0) and (self.df.at[idSymbol,"a4"]>0) and (ask_x>0) and (bid_x>0);
        
        if prices_ok:
#            print("prices ok for ",idSymbol, "ask/bid mean:",ask_mean,bid_mean, "ask/bid:", ask_x, bid_x);
            if side=="BUY":
                # ask is decreased rapidly, so buy at at this ask
                if ask_x<(ask_mean - (self.price_step*5)):
                    price=round((round(ask_x/self.price_step,0)+self.buy_offset)*self.price_step,2);
                    print("buy ask_x:",ask_x," < ask mean:",ask_mean+(self.price_step*3), "@",price);
            
            if side=="SELL": 
                # bid_x>(bid_mean + (self.price_step*5)) or
                if  (bid_x > (self.df.at[idSymbol,"price_open"]+(self.price_step*self.sell_offset))) and (self.df.at[idSymbol,"price_open"]>0):
                    price=round((round(bid_x/self.price_step,0)+self.sell_offset)*self.price_step,2);
                    print("sell bid_x:",bid_x,"> bid mean:",bid_mean+(self.price_step*3), "@",price);
            
        else:
            price=-1;
            
    if algo=="latte":
        # stat arbitrage for first and second option. 

        ask_x=self.df.at[idSymbol,"ask"];
        bid_x=self.df.at[idSymbol,"bid"];
        ask_mean=self.df.at[idSymbol,"ask_mean"];
        bid_mean=self.df.at[idSymbol,"bid_mean"];
        # check if data are ok
        prices_ok=(self.df.at[idSymbol,"b4"]>0) and (self.df.at[idSymbol,"a4"]>0) and (ask_x>0) and (bid_x>0);
        
        if prices_ok:
#            print("prices ok for ",idSymbol, "ask/bid mean:",ask_mean,bid_mean, "ask/bid:", ask_x, bid_x);
            if side=="BUY":
                # ask is decreased rapidly, so buy at at this ask
                if ask_x<(ask_mean - (self.price_step*5)):
                    price=round((round(ask_x/self.price_step,0)+self.buy_offset)*self.price_step,2);
                    print("buy ask_x:",ask_x," < ask mean:",ask_mean+(self.price_step*3), "@",price);
            
            if side=="SELL": 
                # bid_x>(bid_mean + (self.price_step*5)) or
                if  (bid_x > (self.df.at[idSymbol,"price_open"]+(self.price_step*self.sell_offset))) and (self.df.at[idSymbol,"price_open"]>0):
                    price=round((round(bid_x/self.price_step,0)+self.sell_offset)*self.price_step,2);
                    print("sell bid_x:",bid_x,"> bid mean:",bid_mean+(self.price_step*3), "@",price);
            
        else:
            price=-1;
    
    return price;
       
           


