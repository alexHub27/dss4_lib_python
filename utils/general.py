import dataiku as dk 
import datetime as dt
import requests as rq
import json
from multiprocessing import Pool
from bs4 import BeautifulSoup as Soup


def assess_type(test):
    if not test or test!=test :
        return 'NULL'
    try :
        int(test)
        return 'INT'
    except ValueError:
        pass
    try:
        float(test)
        return 'FLOAT'
    except ValueError:
        pass
    
    return 'TEXT'

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def get_soup(link,headerName=None,params=None,verify=None):
    """ The deaders have to be defined as a custom variables at the project level. """
    if headerName: 
        headers = json.loads(dk.get_custom_variables()[headerName])
    else:
        headers = None 
        
    if not verify :
        r = rq.get(link,headers=headers,params=params)
    else:
        r = rq.get(link,headers=headers,params=params,verify=verify)
    soup = Soup(r.text,'html.parser')
    return soup

def get_schema(lst):
    """ Build a standard dataiku.Dataset schema. """
    
    def prepare_schema(el):
        if type(el)!= tuple:
            return (el,"string")
        else:
            return el
        
    lstSch = [prepare_schema(el) for el in lst]
    return [{"name":l[0],"type":l[1]} for l in lst]

def make_date_from_timedelta(d=1):
    """ Build a string from a given number of days prior today. """
    d_ = dt.datetime.now() - dt.timedelta(days=d)
    return dt.datetime.strftime(d_,"%Y-%m-%d")

def pooling(fct,lst,nb_pool=10):
    """Open different pools for the same function. Return the output of each pool in a list"""
    p = Pool(nb_pool)
    infos = p.map(fct,lst)
    p.terminate()
    p.join()
    return infos

def save_model(modelName,model):
    model_json = model.to_json()
    with open("{0}.json".format(modelName),"wb") as f:
        f.write(model_json)
    model.save_weights("{0}.h5".format(modelName))
    print "Model {0} saved on disk".format(modelName)
    return None

def load_model(modNm):
    from keras.models import model_from_json
    with open(modNm+'.json','rb') as f:
        modStr = f.read()
    model = model_from_json(modStr)
    model.load_weights(modNm+'.h5')
    return model

def get_showered(dirtyPig):
    return str(dirtyPig.encode('utf-8')).translate(None,"\r\n\t").strip(' ').decode('utf-8')