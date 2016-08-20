import requests
from bs4 import BeautifulSoup as bs
from elecos import query

QUERY_URL = 'http://esquery.tku.edu.tw/acad/query_result.asp'

def query_by_course_id(id):
    r = requests.get(QUERY_URL, {'func':'go','R1':7,'id':str(id)})
    r.encoding = 'Big5'
    s = bs(r.text,"lxml")
    return s

def watch(session, id, func):
    soup = query(session, id)
    if False:
        func()
