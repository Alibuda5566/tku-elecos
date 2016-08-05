# -*- coding: utf-8 -*-
# @Author: Anthony
# @Date:   2016-02-25 20:07:33
# @Last Modified by:   Anthony
# @Last Modified time: 2016-02-25 20:34:29

import requests
from bs4 import BeautifulSoup
import sys

def safeprint(*s):
    try:
        print(*s)
    except:
        try:
            print(' '.join([str(x) for x in s]).encode('utf8').decode(sys.stdout.encoding))
        except Exception as e:
            print('---- Unable to Print ----')

url_login = "http://www.ais.tku.edu.tw/elecos/login.aspx"
url_action = "http://www.ais.tku.edu.tw/elecos/action.aspx"
headers = {'User-Agent': 'Mozilla/5.0'}
login_payload = dict(
__EVENTTARGET ="btnLogin",
__EVENTARGUMENT = "",
__VIEWSTATE = "/wEPDwULLTE0ODk3NTI0NDMPZBYCAgMPZBYSAgMPDxYCHgRUZXh0BSsxMDQg5a245bm05bqm56ysIDIg5a245pyfIC0g6YG46Kqy5Yqg6YCA6YG4ZGQCBA8PFgIfAGVkZAIMDw9kFgIeB29uY2xpY2sFOWphdmFzY3JpcHQ6dGhpcy5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuTG9naW4nLCcnKWQCDg8WAh8ABboBIOiri+i8uOWFpeWtuOiZn+WPiuWvhueivC4uLjxmb250IHN0eWxlPSJDT0xPUjogcmVkOyBmb250LXdlaWdodDogYm9sZCI+KOOAjOa3oeaxn+Wkp+WtuOWWruS4gOeZu+WFpShTU08p44CN5Zau5LiA5biz5a+G6amX6K2J5a+G56K8O+mgkOioreeCuui6q+WIhuitieaIluWxheeVmeitieW+jO+8lueivCkgPGJyLz48L2ZvbnQ+ZAIQDxYCHwAFcTxmb250IGZhY2U9Iuaomealt+mrlCIgc2l6ZT0iNCI+Ny7liqDpgIDpgbjlvozvvIzmraPlvI/pgbjoqrLlsI/ooajmnIPpgIHoh7PlkITns7vmiYDovYnkuqTlkIzlrbjjgII8L2ZvbnQ+PGJyIC8+ZAISDxYCHwAFtQE8Zm9udCBmYWNlPSLmqJnmpbfpq5QiIHNpemU9IjQiPjgu5pyf5Lit6YCA6YG45q+P5a245pyf5Lul5LqM56eR54K66ZmQ77yM5LiU6YCA6YG45b6M5LiN5b6X5L2O5L+uKOiri+ips+acrOagoeWtuOeUn+acn+S4remAgOmBuOWvpuaWveimgem7ninvvIzoq4vlr6nmhY7opo/lioPpgbjoqrLjgII8L2ZvbnQ+PGJyIC8+ZAIUDxYCHwAFpAE8Zm9udCBmYWNlPSLmqJnmpbfpq5QiIHNpemU9IjQiPjku6YC+5a245pyf5LiK6Kqy6YGU5LiJ5YiG5LmL5LiA5pmC5aeL6YCA6YG477yM5L6d6KaP5a6a5oeJ57mz5Lqk5LmL5a245YiG6LK75LiN5LqI6YCA6YKE77yM5pyq57mz5a245YiG6LK76ICF5oeJ5LqI6KOc57mz44CCPC9mb250PmQCFg8WAh8ABYIBPGZvbnQgZmFjZT0i5qiZ5qW36auUIiBzaXplPSI0Ij4zLuacrOezu+e1seWPquaPkOS+m+mBuOiqsuaJgOmcgCzlhbblroPpgbjoqrLnm7jpl5zlip/og70s6KuL6Iez55u46Zec57ay56uZ5L2/55So44CCPC9mb250PjxiciAvPmQCGA8PFgIfAAUKMS4xNjkuMC43MGRkZLCvxudmyixSmC2yC2hmfHFaC4mi",
__VIEWSTATEGENERATOR = "F118B446",
__EVENTVALIDATION = "/wEWBAKmq+68BgKA7M65CgL79NvIBAKC3IeGDDbApj0FJlrwl9T/00R/PJtgIbSa",
txtStuNo = "",
txtPSWD = ""
)
action_payload = dict(
__EVENTTARGET ="",
__EVENTARGUMENT = "",
__VIEWSTATE = "/wEPDwUKLTMxODQyODM0Nw9kFgICAw9kFigCAQ8PFgIeBFRleHRlZGQCAw8PFgIfAAUrMTA0IOWtuOW5tOW6puesrCAyIOWtuOacnyAtIOmBuOiqsuWKoOmAgOmBuGRkAgUPDxYCHwAFCTQwNDg1NDAxOWRkAgcPDxYCHwAFCeWCheaiteiNu2RkAgkPDxYCHwAFGlRRSUNCMSAg6LOH5Ym157O76Luf5bel5LiAZGQCDQ8WAh8ABTEuLi4uIOiri+i8uOWFpemWi+iqsuW6j+iZn+W+jCwg5YaN5oyJ5Yqf6IO96Y21Li4uZAIPDw9kFgIeB29uY2xpY2sF/wFqYXZhc2NyaXB0OnRoaXMuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRGVsIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuT2ZmZXIiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5FbGVDb3MiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5Mb2dvdXQiKS5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuQWRkJywnJylkAhEPD2QWAh8BBf8BamF2YXNjcmlwdDp0aGlzLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkFkZCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bk9mZmVyIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRWxlQ29zIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuTG9nb3V0IikuZGlzYWJsZWQ9dHJ1ZTtfX2RvUG9zdEJhY2soJ2J0bkRlbCcsJycpZAITDw9kFgIfAQX/AWphdmFzY3JpcHQ6dGhpcy5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5BZGQiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5EZWwiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5FbGVDb3MiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5Mb2dvdXQiKS5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuT2ZmZXInLCcnKWQCFQ8PZBYCHwEF/wFqYXZhc2NyaXB0OnRoaXMuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuQWRkIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRGVsIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuT2ZmZXIiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5Mb2dvdXQiKS5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuRWxlQ29zJywnJylkAhcPD2QWAh8BBYABamF2YXNjcmlwdDp0aGlzLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkFkZCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bk9mZmVyIikuZGlzYWJsZWQ9dHJ1ZTtkAhkPD2QWAh8BBf8BamF2YXNjcmlwdDp0aGlzLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkFkZCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkRlbCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bk9mZmVyIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRWxlQ29zIikuZGlzYWJsZWQ9dHJ1ZTtfX2RvUG9zdEJhY2soJ2J0bkxvZ291dCcsJycpZAIbDxYCHwBlZAIdDzwrAA0BAA8WAh4HVmlzaWJsZWhkZAIfDxYCHwBlZAIhDzwrAA0BAA8WAh8CaGRkAiMPFgIfAAUb5oKo55qE6YG4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",
__VIEWSTATEGENERATOR = "2E66DAD8",
__EVENTVALIDATION = "/wEWCAKZu8TqAgKsvM32BgKMk4HYDwKLk6XGBQKft6B4AuKZlo8DAr/Bm5QOAqbgzZ0J7U1LWr1/0YV3UKJOU8cINfwIO00=",
txtCosEleSeq = ""
)
def login(session,usr,pwd,fail_msg=True,timetable=True):
    login_payload['txtStuNo'] =usr
    login_payload['txtPSWD']  =pwd
    r = session.post(url_login,headers=headers,data=login_payload)
    soup = BeautifulSoup(r.content,"html.parser")
    if '.EleCos' in session.cookies.keys():
        safeprint('\n===== Login Success =====')
        safeprint(soup.findAll('p')[0].text.replace('\t','').replace('\xa0','').replace(' ',''))
        if timetable: print_timetabe(soup)
        return True
    if fail_msg: safeprint('===== Login Failed =====')
    if fail_msg: safeprint(s.findAll('tr')[4].findAll('td')[1].text.strip())
    return False
def action(session,method,cosid):
    cosid = str(cosid)
    action_payload['__EVENTTARGET'] = "btnDel" if method == "del" else "btnAdd"
    action_payload['txtCosEleSeq'] = cosid
    r = session.post(url_action,headers=headers,data=action_payload)
    soup = BeautifulSoup(r.content,"html.parser")
    msg = get_msg(soup)
    safeprint(">>>> " + ("Del " if method == "del" else "Add ") + cosid)
    safeprint(msg)
    if msg.startswith("E999"):
        return False
    return soup
def query(session,cosid):
    cosid = str(cosid)
    action_payload['__EVENTTARGET'] = "btnOffer"
    action_payload['txtCosEleSeq'] = cosid
    r = session.post(url_action,headers=headers,data=action_payload)
    soup = BeautifulSoup(r.content,"html.parser")
    safeprint(get_msg(soup))
    return r
def get_msg(action_soup):
    return action_soup.findAll('tr')[1].findAll('td')[2].text.strip()
def print_timetabe(action_soup):
    safeprint('================== My Elecos ==================')
    try:
        ctds = lambda tds: ' | '.join(tds[:4] + [tds[12]] + [tds[10]] + [tds[4]] + tds[13].split(' '))
        ptd = lambda td: ctds([x.text.strip() for x in td])
        clean = lambda x: x.replace('\t','').replace('\xa0','').strip()
        [safeprint(r) for r in (ptd(x.findAll('td')) for x in action_soup.findAll('tr')[4:-2])]
    except:
        pass

if __name__ == '__main__':
    from configs import *
    from datetime import datetime, time
    from time import sleep

    def wait_start(runTime, action):
        while runTime > datetime.now():
            sleep(interval)
        return action()

    def fuck_elecos():
        session = requests.Session()
        for x in range(1,try_times + 1):
            try:
                safeprint('[{}] Trys'.format(x))
                if login(session,student_no,password,False,True):
                    break
            except Exception as e:
                safeprint(e)
            sleep(1)
        s = None
        if not '.EleCos' in session.cookies.keys():
            safeprint('\n========== Failed too many times, Exiting ==========')
        if len(dels):
            safeprint('\n========== Start Deleting({}) =========='.format(len(dels)))
            for d in dels:
                s = action(session,"del",d)
        if len(adds):
            safeprint('\n========== Start Adding({}) =========='.format(len(adds)))
            for a in adds:
                s = action(session,"add",a)

        if s:
            print_timetabe(s)
        safeprint('\n========== Task Complete, Exiting ==========')

    start_time = datetime(*start_time)
    safeprint('Current:',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    safeprint('[!] The program will start at {} , do NOT abort.'.format(start_time.strftime("%Y-%m-%d %H:%M:%S")))
    sleep(1)
    wait_start(start_time, lambda: fuck_elecos())
