import dataiku as dk 
import datetime as dt
import requests as rq
import json
from multiprocessing import Pool
from bs4 import BeautifulSoup as Soup

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def get_soup(link,headerName):
    """ The deaders have to be defined as a custom variables at the project level. """
    headers = json.loads(dk.get_custom_variables()[headerName])
    r = rq.get(link,headers=headers)
    soup = Soup(r.text,'html.parser')
    return soup

def get_schema(lst):
    """ Build a standard dataiku.Dataset schema. """
    return [{"name":l,"type":"string"} for l in lst]

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