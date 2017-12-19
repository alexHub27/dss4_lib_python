import quandl as qd

def get_data_from_quand(tick,start_date="2004-12-31",end_date="2017-06-30"):
    qd.ApiConfig.api_key = 'w-DrTrcoKxr4oxczgsTB'
    mydata =  qd.get(['WIKI/{0}'.format(tick)],start_date=start_date,end_date=end_date)
    print "Getting data from quandl for {0} from {1} to {2} - {3} lines retrieved from {4} to {5}".format(tick,startDate,endDate,mydata.shape[0],mydata.index[0],mydata.index[-1])
    mydata = mydata.reset_index()
    return mydata

def get_dic_from_quandl(mydata):
    keys = [k.split(' - ')[-1].lower().replace(' ','').replace('.','_').replace('-','_') for k in mydata.columns]
    return [dict((keys[i],v) for i,v in enumerate(row)) for row in mydata.values]