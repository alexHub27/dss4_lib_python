import quandl as qd

def get_data_from_quandl(tick,startDate="2004-12-31",endDate="2017-06-30"):
    qd.ApiConfig.api_key = 'w-DrTrcoKxr4oxczgsTB'
    mydata =  qd.get(['WIKI/{0}'.format(tick)],start_date=startDate,end_date=endDate)
    print "Getting data from quandl for {0} from {1} to {2} - {3} lines retrieved from {4} to {5}".format(tick,startDate,endDate,mydata.shape[0],mydata.index[0],mydata.index[-1])
    mydata = mydata.reset_index()
    return mydata

def get_dic_from_quandl(mydata):
    keys = [k.split(' - ')[-1].lower().replace(' ','').replace('.','_').replace('-','_') for k in mydata.columns]
    return [dict((keys[i],v) for i,v in enumerate(row)) for row in mydata.values]

def get_keys_from_quandl():
    # fake call to jsut get a data frame and make some transformation on it
    tick,start_date,end_date="AAPL","2004-12-31","2005-01-30"
    mydata = get_data_from_quandl(tick,start_date,end_date)
    return [k.split(' - ')[-1].lower().replace(' ','').replace('.','_').replace('-','_') for k in mydata.columns]
    
    