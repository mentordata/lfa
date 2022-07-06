from datetime import datetime
from numpy import dtype
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re

class IBKRSpider(scrapy.Spider):
    name = 'dataSpider'

    # V2TX
    #start_urls = ['https://misc.interactivebrokers.com/cstools/contract_info/v3.10/index.php?action=Futures%20Option%20Chain&entityId=a27601002&lang=en&ib_entity=&wlId=IB&showEntities=Y']

    # VIX
    #start_urls = ['https://misc.interactivebrokers.com/cstools/contract_info/v3.10/index.php?filter=5F6Jyg&csaction=Search+Form&action=Option+Chain&ib_entity=&conid=0&contract_id=&noBanner=&rescnt=100&sortBy=description&sortDir=ASC&start=1&contractType=&country=&currency=&description=&entityId=a19207303&exchange=&exchanges=&hasBond=&hasFut=&hasOpt=&hasWar=&initMarginLow=&initMarginHigh=&maintMarginLow=&maintMarginHigh=&shortMarginLow=&shortMarginHigh=&secId=&secIdType=&tradeInFractions=&symbol=&showEntities=Y&bondIssueDateHigh=&bondIssueDateLow=&bondIssuer=&bondMaturityDateHigh=&bondMaturityDateLow=&bondType=&collateralType=&couponType=&futuresType=&futExpDateHigh=&futExpDateLow=&indexType=&fundFamily=&investType=&optExerciseStyle=&optExpDateHigh=&optExpDateLow=&optStrikeHigh=&optStrikeLow=&oeds=&oede=&or=&shortable=&stockType=&warExerciseStyle=&warExpDateHigh=&warExpDateLow=&warIssueDateHigh=&warIssueDateLow=&warIssuer=&warRight=&warStrikeHigh=&warStrikeLow=&ioptExerciseStyle=&ioptExpDateHigh=&ioptExpDateLow=&ioptIssueDateHigh=&ioptIssueDateLow=&ioptIssuer=&ioptRight=&ioptKnockoutHigh=&ioptKnockoutLow=&ioptStrikeHigh=&ioptStrikeLow=&sec_id_type=&key=&val=&site=IB&wlId=IB&defaultWlId=IB&wlShortName=IB&wlLongName=Interactive+Brokers&prefLang=en&lang=en']

    # DAX
    start_urls = ['https://misc.interactivebrokers.com/cstools/contract_info/v3.10/index.php?action=Option%20Chain&entityId=a19206562&lang=en&ib_entity=&wlId=IB&showEntities=Y']

    # SPX
    #start_urls = ['https://contract.ibkr.info/v3.10/index.php?action=Option%20Chain&entityId=a19206582&lang=en&ib_entity=&wlId=GEN&showEntities=Y']

    def parse(self, response):

        table = response.xpath('//*[@class="resultsTbl table table-bordered"]//tr')
        #print(table)
        
        items = []     
        _days_val = 0
        _dateExpir = ''
        for opt_fut in table[7:]:
            if(len(opt_fut.xpath('td').extract()) == 3):
                #checking reamining "Days to Exp."
                _days = str(opt_fut.xpath('td/center').extract())
                m = re.search('Exp.</b>:(.+?)<b>Ex', _days)
                _days_val = int(m.group(1))
                print("DAYS REMAINING",_days_val)
                if(_days_val <= 0 or _days_val == None):
                    continue
                if(_days_val >= 366):
                    print("EXPIRATION DATE IS OVER 365 DAYS. CLOSING PROGRAM.")
                    break
                else:
                    _dateE = str(opt_fut.xpath('td/center').extract())
                    m = re.search('tion</b>: (.+?) <b>Day', _dateE)
                    _dateExpir = str(m.group(1))
            
            # getting data from correct records
            if(len(opt_fut.xpath('td').extract()) == 8 and str(opt_fut.xpath('td')[3].extract()) != 'Strike'): # and float(opt_fut.xpath('td/text()')[2].extract()) >=20 and float(opt_fut.xpath('td/text()')[2].extract()) <=40 ):
            #getting conid for call/put
                callData = str(opt_fut.xpath('td')[0].extract())
                n = re.search("Conid: (.+?)\\\'",callData)
                callConid = int(n.group(1))

                putData = str(opt_fut.xpath('td')[7].extract())
                n = re.search("Conid: (.+?)\\\'",putData)
                putConid = int(n.group(1))

                item = {
                    'callConid': callConid,
                    'clocal_name': str(opt_fut.xpath('td/b/a/text()')[0].extract()), #.replace(" ","_"),
                    'clocal_class': opt_fut.xpath('td/text()')[0].extract(),
                    'call_close_prc': opt_fut.xpath('td/text()')[1].extract(),
                    'strike': float(opt_fut.xpath('td/text()')[2].extract()),
                    'multiplier': opt_fut.xpath('td/text()')[3].extract(),
                    'put_close_prc': opt_fut.xpath('td/text()')[4].extract(),
                    'plocal_class': opt_fut.xpath('td/text()')[5].extract(),
                    'plocal_name': str(opt_fut.xpath('td/b/a/text()')[1].extract()), #.replace(" ","_"),
                    'putConid': putConid,
                    'expiration': _dateExpir
                }
                #print("\n-------------------------------------------------------------------\n")
                #print(item)
                # yield {'row':item}
                items.append(item)

        df = pd.DataFrame(items,columns=['callConid','clocal_name','clocal_class','call_close_prc','strike','multiplier','put_close_prc','plocal_class','plocal_name','putConid','expiration'])
        #yield df.to_csv("ibkr_OPT_VIX.csv",sep=",",index=False)
        yield df.to_csv("ibkr_dax.csv",sep=",",index=False)
        #print(df.dtypes)


if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(IBKRSpider)
  process.start()