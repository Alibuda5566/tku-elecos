# -*- coding: utf-8 -*-
# @Author: Anthony
# @Date:   2016-02-25 20:07:33
# @Last Modified by:   Anthony
# @Last Modified time: 2016-02-25 20:34:29

import requests
from bs4 import BeautifulSoup
import sys
from   termcolor import colored, cprint
import time

def safeprint(*args, color=None, back=None, attrs=None, **kwargs):
    try:
        cprint(' '.join([str(x) for x in args]), color, back, attrs=attrs, **kwargs)
    except:
        try:
            print(' '.join([str(x) for x in args]).encode('utf8').decode(sys.stdout.encoding), **kwargs)
        except Exception as e:
            print(e)

URL_LOGIN = "http://www.ais.tku.edu.tw/elecos/login.aspx"
URL_ACTION = "http://www.ais.tku.edu.tw/elecos/action.aspx"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
LOGIN_PAYLOAD = dict(
__EVENTTARGET ="btnLogin",
__EVENTARGUMENT = "",
__VIEWSTATE = "/wEPDwULLTE0ODk3NTI0NDMPZBYCAgMPZBYSAgMPDxYCHgRUZXh0BSsxMDQg5a245bm05bqm56ysIDIg5a245pyfIC0g6YG46Kqy5Yqg6YCA6YG4ZGQCBA8PFgIfAGVkZAIMDw9kFgIeB29uY2xpY2sFOWphdmFzY3JpcHQ6dGhpcy5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuTG9naW4nLCcnKWQCDg8WAh8ABboBIOiri+i8uOWFpeWtuOiZn+WPiuWvhueivC4uLjxmb250IHN0eWxlPSJDT0xPUjogcmVkOyBmb250LXdlaWdodDogYm9sZCI+KOOAjOa3oeaxn+Wkp+WtuOWWruS4gOeZu+WFpShTU08p44CN5Zau5LiA5biz5a+G6amX6K2J5a+G56K8O+mgkOioreeCuui6q+WIhuitieaIluWxheeVmeitieW+jO+8lueivCkgPGJyLz48L2ZvbnQ+ZAIQDxYCHwAFcTxmb250IGZhY2U9Iuaomealt+mrlCIgc2l6ZT0iNCI+Ny7liqDpgIDpgbjlvozvvIzmraPlvI/pgbjoqrLlsI/ooajmnIPpgIHoh7PlkITns7vmiYDovYnkuqTlkIzlrbjjgII8L2ZvbnQ+PGJyIC8+ZAISDxYCHwAFtQE8Zm9udCBmYWNlPSLmqJnmpbfpq5QiIHNpemU9IjQiPjgu5pyf5Lit6YCA6YG45q+P5a245pyf5Lul5LqM56eR54K66ZmQ77yM5LiU6YCA6YG45b6M5LiN5b6X5L2O5L+uKOiri+ips+acrOagoeWtuOeUn+acn+S4remAgOmBuOWvpuaWveimgem7ninvvIzoq4vlr6nmhY7opo/lioPpgbjoqrLjgII8L2ZvbnQ+PGJyIC8+ZAIUDxYCHwAFpAE8Zm9udCBmYWNlPSLmqJnmpbfpq5QiIHNpemU9IjQiPjku6YC+5a245pyf5LiK6Kqy6YGU5LiJ5YiG5LmL5LiA5pmC5aeL6YCA6YG477yM5L6d6KaP5a6a5oeJ57mz5Lqk5LmL5a245YiG6LK75LiN5LqI6YCA6YKE77yM5pyq57mz5a245YiG6LK76ICF5oeJ5LqI6KOc57mz44CCPC9mb250PmQCFg8WAh8ABYIBPGZvbnQgZmFjZT0i5qiZ5qW36auUIiBzaXplPSI0Ij4zLuacrOezu+e1seWPquaPkOS+m+mBuOiqsuaJgOmcgCzlhbblroPpgbjoqrLnm7jpl5zlip/og70s6KuL6Iez55u46Zec57ay56uZ5L2/55So44CCPC9mb250PjxiciAvPmQCGA8PFgIfAAUKMS4xNjkuMC43MGRkZLCvxudmyixSmC2yC2hmfHFaC4mi",
__VIEWSTATEGENERATOR = "F118B446",
__EVENTVALIDATION = "/wEWBAKmq+68BgKA7M65CgL79NvIBAKC3IeGDDbApj0FJlrwl9T/00R/PJtgIbSa",
txtStuNo = "",
txtPSWD = ""
)
ACTION_PAYLOAD = dict(
__EVENTTARGET ="",
__EVENTARGUMENT = "",
__VIEWSTATE = "/wEPDwUKLTMxODQyODM0Nw9kFgICAw9kFigCAQ8PFgIeBFRleHRlZGQCAw8PFgIfAAUrMTA0IOWtuOW5tOW6puesrCAyIOWtuOacnyAtIOmBuOiqsuWKoOmAgOmBuGRkAgUPDxYCHwAFCTQwNDg1NDAxOWRkAgcPDxYCHwAFCeWCheaiteiNu2RkAgkPDxYCHwAFGlRRSUNCMSAg6LOH5Ym157O76Luf5bel5LiAZGQCDQ8WAh8ABTEuLi4uIOiri+i8uOWFpemWi+iqsuW6j+iZn+W+jCwg5YaN5oyJ5Yqf6IO96Y21Li4uZAIPDw9kFgIeB29uY2xpY2sF/wFqYXZhc2NyaXB0OnRoaXMuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRGVsIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuT2ZmZXIiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5FbGVDb3MiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5Mb2dvdXQiKS5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuQWRkJywnJylkAhEPD2QWAh8BBf8BamF2YXNjcmlwdDp0aGlzLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkFkZCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bk9mZmVyIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRWxlQ29zIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuTG9nb3V0IikuZGlzYWJsZWQ9dHJ1ZTtfX2RvUG9zdEJhY2soJ2J0bkRlbCcsJycpZAITDw9kFgIfAQX/AWphdmFzY3JpcHQ6dGhpcy5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5BZGQiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5EZWwiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5FbGVDb3MiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5Mb2dvdXQiKS5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuT2ZmZXInLCcnKWQCFQ8PZBYCHwEF/wFqYXZhc2NyaXB0OnRoaXMuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuQWRkIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRGVsIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuT2ZmZXIiKS5kaXNhYmxlZD10cnVlO2RvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG5Mb2dvdXQiKS5kaXNhYmxlZD10cnVlO19fZG9Qb3N0QmFjaygnYnRuRWxlQ29zJywnJylkAhcPD2QWAh8BBYABamF2YXNjcmlwdDp0aGlzLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkFkZCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bk9mZmVyIikuZGlzYWJsZWQ9dHJ1ZTtkAhkPD2QWAh8BBf8BamF2YXNjcmlwdDp0aGlzLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkFkZCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bkRlbCIpLmRpc2FibGVkPXRydWU7ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bk9mZmVyIikuZGlzYWJsZWQ9dHJ1ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuRWxlQ29zIikuZGlzYWJsZWQ9dHJ1ZTtfX2RvUG9zdEJhY2soJ2J0bkxvZ291dCcsJycpZAIbDxYCHwBlZAIdDzwrAA0BAA8WAh4HVmlzaWJsZWhkZAIfDxYCHwBlZAIhDzwrAA0BAA8WAh8CaGRkAiMPFgIfAAUb5oKo55qE6YG46Kqy6LOH5paZ77yaPGJyIC8+ZAIlDzwrAA0BAA8WBB4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudAIKZBYCZg9kFhYCAQ9kFiBmDw8WAh8ABQQyMTAzZGQCAQ8PFgIfAAUFVEdOUEJkZAICDw8WAh8ABQExZGQCAw8PFgIfAAUFVDk4NzRkZAIEDw8WAh8ABSTnlLfvvI7lpbPnlJ/pq5TogrLvvI3moYznkIPoiIjotqPnj61kZAIFDw8WAh8ABQEgZGQCBg8PFgIfAAUBMGRkAgcPDxYCHwAFAkIgZGQCCA8PFgIfAAUCICBkZAIJDw8WAh8ABQFBZGQCCg8PFgIfAAUBMGRkAgsPDxYCHwAFAiAgZGQCDA8PFgIfAAUh6Zmz5Yex5pm6ICAgICAgICAgICAgICAgICAgICAgICAgZGQCDQ8PFgIfAAUh5LqULzAzLDA0Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7ZGQCDg8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIPDw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAgIPZBYgZg8PFgIfAAUEMzg3OWRkAgEPDxYCHwAFBVRRSUNCZGQCAg8PFgIfAAUBMWRkAgMPDxYCHwAFBUgwMDA1ZGQCBA8PFgIfAAUS6Iux5paH5Y+j6Kqe5rqd6YCaZGQCBQ8PFgIfAAUBIGRkAgYPDxYCHwAFATBkZAIHDw8WAh8ABQJBIGRkAggPDxYCHwAFAiAgZGQCCQ8PFgIfAAUBQWRkAgoPDxYCHwAFATJkZAILDw8WAh8ABQIgIGRkAgwPDxYCHwAFIeaWveaHv+iKuSAgICAgICAgICAgICAgICAgICAgICAgIGRkAg0PDxYCHwAFLeWbmy8wNiwwNyZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzMwMiZuYnNwO2RkAg4PDxYCHwAFIDxGT05UIHN0eWxlPSJDT0xPUjogcmVkIj48L0ZPTlQ+ZGQCDw8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIDD2QWIGYPDxYCHwAFBDM4ODRkZAIBDw8WAh8ABQVUUUlDQmRkAgIPDxYCHwAFATFkZAIDDw8WAh8ABQVTMDQzOWRkAgQPDxYCHwAFDOe3muaAp+S7o+aVuGRkAgUPDxYCHwAFASBkZAIGDw8WAh8ABQEwZGQCBw8PFgIfAAUCQSBkZAIIDw8WAh8ABQIgIGRkAgkPDxYCHwAFAUFkZAIKDw8WAh8ABQEzZGQCCw8PFgIfAAUCICBkZAIMDw8WAh8ABSHmnLHjgIDnlZkgICAgICAgICAgICAgICAgICAgICAgICBkZAINDw8WAh8ABXTkuIAvMDYmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsvQ0wmbmJzcDs0MDEmbmJzcDs8YnImbmJzcDsvPuWbmy8wOCwwOSZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzQwMSZuYnNwO2RkAg4PDxYCHwAFIDxGT05UIHN0eWxlPSJDT0xPUjogcmVkIj48L0ZPTlQ+ZGQCDw8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIED2QWIGYPDxYCHwAFBDM4ODVkZAIBDw8WAh8ABQVUUUlDQmRkAgIPDxYCHwAFATFkZAIDDw8WAh8ABQVTMDQ1MGRkAgQPDxYCHwAFCeapn+eOh+irlmRkAgUPDxYCHwAFASBkZAIGDw8WAh8ABQEwZGQCBw8PFgIfAAUCQSBkZAIIDw8WAh8ABQIgIGRkAgkPDxYCHwAFAUFkZAIKDw8WAh8ABQEzZGQCCw8PFgIfAAUCICBkZAIMDw8WAh8ABSHmnLHjgIDnlZkgICAgICAgICAgICAgICAgICAgICAgICBkZAINDw8WAh8ABXTkuIAvMDEsMDImbmJzcDsmbmJzcDsmbmJzcDsvQ0wmbmJzcDs0MDQmbmJzcDs8YnImbmJzcDsvPuS4iS8wNCZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzQwNCZuYnNwO2RkAg4PDxYCHwAFIDxGT05UIHN0eWxlPSJDT0xPUjogcmVkIj48L0ZPTlQ+ZGQCDw8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIFD2QWIGYPDxYCHwAFBDM4ODZkZAIBDw8WAh8ABQVUUUlDQmRkAgIPDxYCHwAFATFkZAIDDw8WAh8ABQVUMjYzN2RkAgQPDxYCHwAFJOekvuWcmOWtuOe/kuiIh+WvpuS9nO+8jeWFpemWgOiqsueoi2RkAgUPDxYCHwAFASBkZAIGDw8WAh8ABQEwZGQCBw8PFgIfAAUCQSBkZAIIDw8WAh8ABQIgIGRkAgkPDxYCHwAFAUFkZAIKDw8WAh8ABQExZGQCCw8PFgIfAAUCSyBkZAIMDw8WAh8ABSHpu4PmlofmmbogICAgICAgICAgICAgICAgICAgICAgICBkZAINDw8WAh8ABS3kuowvMDgsMDkmbmJzcDsmbmJzcDsmbmJzcDsvQ0wmbmJzcDsxMDEmbmJzcDtkZAIODw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAg8PDxYCHwAFIDxGT05UIHN0eWxlPSJDT0xPUjogcmVkIj48L0ZPTlQ+ZGQCBg9kFiBmDw8WAh8ABQQzODg3ZGQCAQ8PFgIfAAUFVFFJQ0JkZAICDw8WAh8ABQExZGQCAw8PFgIfAAUFVDk2MDhkZAIEDw8WAh8ABSTmoKHlnJLoiIfnpL7ljYDmnI3li5nlrbjnv5LvvIjkuIDvvIlkZAIFDw8WAh8ABQEgZGQCBg8PFgIfAAUBMmRkAgcPDxYCHwAFAkEgZGQCCA8PFgIfAAUCICBkZAIJDw8WAh8ABQFBZGQCCg8PFgIfAAUBMGRkAgsPDxYCHwAFAiAgZGQCDA8PFgIfAAUh5p2O5ZyL5Z+6ICAgICAgICAgICAgICAgICAgICAgICAgZGQCDQ8PFgIfAAUw5LqMLzAxJm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7ZGQCDg8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIPDw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAgcPZBYgZg8PFgIfAAUEMzg5NmRkAgEPDxYCHwAFBVRRSUNCZGQCAg8PFgIfAAUBMmRkAgMPDxYCHwAFBVAwMDA3ZGQCBA8PFgIfAAUS6ZaL5pS+6Luf6auU5a+m5YuZZGQCBQ8PFgIfAAUBIGRkAgYPDxYCHwAFATBkZAIHDw8WAh8ABQJBIGRkAggPDxYCHwAFAiAgZGQCCQ8PFgIfAAUBQ2RkAgoPDxYCHwAFATNkZAILDw8WAh8ABQIgIGRkAgwPDxYCHwAFIeW8te6whuiqoCAgICAgICAgICAgICAgICAgICAgICAgIGRkAg0PDxYCHwAFdOS6jC8wMyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzUxOSZuYnNwOzxiciZuYnNwOy8+5LiJLzAxLDAyJm5ic3A7Jm5ic3A7Jm5ic3A7L0NMJm5ic3A7NTE5Jm5ic3A7ZGQCDg8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIPDw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAggPZBYgZg8PFgIfAAUEMzkwMWRkAgEPDxYCHwAFBVRRSUNCZGQCAg8PFgIfAAUBNGRkAgMPDxYCHwAFBU0wOTQ3ZGQCBA8PFgIfAAUM6LOH5paZ5o6i5YuYZGQCBQ8PFgIfAAUBIGRkAgYPDxYCHwAFATBkZAIHDw8WAh8ABQJBIGRkAggPDxYCHwAFAiAgZGQCCQ8PFgIfAAUBQ2RkAgoPDxYCHwAFATNkZAILDw8WAh8ABQIgIGRkAgwPDxYCHwAFIemZs+aDh+WHsSAgICAgICAgICAgICAgICAgICAgICAgIGRkAg0PDxYCHwAFdOS4gC8wOCwwOSZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzQwNyZuYnNwOzxiciZuYnNwOy8+5LqMLzA2Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7L0NMJm5ic3A7MzIzJm5ic3A7ZGQCDg8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIPDw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAgkPZBYgZg8PFgIfAAUEMzkxNWRkAgEPDxYCHwAFBVRRSURCZGQCAg8PFgIfAAUBMmRkAgMPDxYCHwAFBUUwNjQ2ZGQCBA8PFgIfAAUP6LOH5paZ5bqr57O757WxZGQCBQ8PFgIfAAUBIGRkAgYPDxYCHwAFATBkZAIHDw8WAh8ABQJBIGRkAggPDxYCHwAFAiAgZGQCCQ8PFgIfAAUBQWRkAgoPDxYCHwAFATNkZAILDw8WAh8ABQIgIGRkAgwPDxYCHwAFIemZs+aDh+WHsSAgICAgICAgICAgICAgICAgICAgICAgIGRkAg0PDxYCHwAFdOS4gC8wMyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzMyNCZuYnNwOzxiciZuYnNwOy8+5ZubLzAzLDA0Jm5ic3A7Jm5ic3A7Jm5ic3A7L0NMJm5ic3A7NDA3Jm5ic3A7ZGQCDg8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIPDw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAgoPZBYgZg8PFgIfAAUEMzkxNmRkAgEPDxYCHwAFBVRRSURCZGQCAg8PFgIfAAUBMmRkAgMPDxYCHwAFBUUxMTExZGQCBA8PFgIfAAUJ5ryU566X5rOVZGQCBQ8PFgIfAAUBIGRkAgYPDxYCHwAFATBkZAIHDw8WAh8ABQJBIGRkAggPDxYCHwAFAiAgZGQCCQ8PFgIfAAUBQWRkAgoPDxYCHwAFATNkZAILDw8WAh8ABQIgIGRkAgwPDxYCHwAFIea0quW+qeS4gCAgICAgICAgICAgICAgICAgICAgICAgIGRkAg0PDxYCHwAFdOS4iS8wMyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOyZuYnNwOy9DTCZuYnNwOzQwNyZuYnNwOzxiciZuYnNwOy8+5ZubLzAxLDAyJm5ic3A7Jm5ic3A7Jm5ic3A7L0NMJm5ic3A7NDA3Jm5ic3A7ZGQCDg8PFgIfAAUgPEZPTlQgc3R5bGU9IkNPTE9SOiByZWQiPjwvRk9OVD5kZAIPDw8WAh8ABSA8Rk9OVCBzdHlsZT0iQ09MT1I6IHJlZCI+PC9GT05UPmRkAgsPDxYCHwJoZGQCJw8WAh8ABV7vvIrlsI/oqIjvvIombmJzcDsmbmJzcDsmbmJzcDsmbmJzcDvlhbHkv67nv5ImbmJzcDsxMCZuYnNwO+enkSZuYnNwOyZuYnNwOyZuYnNwOzIxJm5ic3A75a245YiGZAIpDw8WAh8ABQwxLjE2OS4wLjcwLTBkZBgDBQlHcmlkVmlldzEPPCsACgEIAgFkBQlHcmlkVmlldzMPZ2QFCUdyaWRWaWV3Mg9nZNM6r7kZTImMAs2AToc/Pog0e8q3",
__VIEWSTATEGENERATOR = "2E66DAD8",
__EVENTVALIDATION = "/wEWCAKZu8TqAgKsvM32BgKMk4HYDwKLk6XGBQKft6B4AuKZlo8DAr/Bm5QOAqbgzZ0J7U1LWr1/0YV3UKJOU8cINfwIO00=",
txtCosEleSeq = ""
)

class Elecos:
    def __init__(self, user = None, password = None):
        self.user = user
        self.password = password
        self.session = requests.Session()

    def login(self, user = None, password = None):
        login_payload = dict(LOGIN_PAYLOAD)
        login_payload['txtStuNo'] = user or self.user
        login_payload['txtPSWD']  = password or self.password
        r = self.session.post(URL_LOGIN,headers=HEADERS,data=login_payload)
        if self.is_login:
            return True, '', None
        soup = None
        try:
            soup = BeautifulSoup(r.content,"html.parser")
            msg = soup.findAll('tr')[4].findAll('td')[1].text.strip()
        except Exception as e:
            msg = str(e)
        return False, msg, soup

    def query(self, cosid):
        cosid = str(cosid)
        action_payload = dict(ACTION_PAYLOAD)
        action_payload['__EVENTTARGET'] = "btnOffer"
        action_payload['txtCosEleSeq'] = cosid
        r = self.session.post(URL_ACTION,headers=HEADERS,data=action_payload)
        soup = BeautifulSoup(r.content,"html.parser")
        msg = get_msg(soup)
        return True, msg, soup

    def action(self,method,cosid):
        cosid = str(cosid)
        action_payload = dict(ACTION_PAYLOAD)
        action_payload['__EVENTTARGET'] = "btnDel" if method == "del" else "btnAdd"
        action_payload['txtCosEleSeq'] = cosid
        r = self.session.post(URL_ACTION,headers=HEADERS,data=action_payload)
        soup = BeautifulSoup(r.content,"html.parser")
        msg = get_msg(soup)
        if msg.startswith("E999") or msg.startswith("[!]"):
            return False, msg, None
        return True, msg, soup

    @property
    def is_login(self):
        return  '.EleCos' in self.session.cookies.keys()


def get_msg(action_soup):
    try:
        return action_soup.findAll('tr')[1].findAll('td')[2].text.strip()
    except Exception as e:
        return '[!] 解析返回信息失敗 "'+str(e)+'"'

def print_timetabe(action_soup):
    if not action_soup:
        return
    safeprint('\n================== 我的選課 ==================', color='grey', back='cyan' )
    try:
        ctds = lambda tds: ' | '.join(tds[:4] + [tds[12]] + [tds[10]] + [tds[4]] + tds[13].split(' '))
        ptd = lambda td: ctds([x.text.strip() for x in td])
        clean = lambda x: x.replace('\t','').replace('\xa0','').strip()
        [safeprint(r) for r in (ptd(x.findAll('td')) for x in action_soup.findAll('tr')[4:-2])]
    except:
        pass

def fuck_elecos(student_no,password,adds=[],dels=[],try_times=180,login_interval=0.3):
    safeprint('=== 程序開始', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '===', color='green')
    elecos = Elecos(student_no, password)
    for x in range(1,try_times + 1):
        #break # TEST
        try:
            safeprint('第 {}/{} 次嘗試登陸'.format(x,try_times), color='cyan', end='')
            result, msg, soup = elecos.login()
            if result:
                safeprint(' [成功] ', color='green')
                print_timetabe(soup)
                break
            else:
                safeprint(' [失敗] ', color='red', end='')
                safeprint(msg, color='yellow')
        except Exception as e:
            safeprint(e)
        time.sleep(login_interval)
    soup = None
    if not elecos.is_login:
        safeprint('\n========== 嘗試多次登陸失敗, 程序結束 ==========', color='white', back='on_red')
        return
    if len(dels):
        safeprint('\n========== 開始退選({}) =========='.format(len(dels)), color='yellow')
        for d in dels:
            try:
                result, msg, soup = elecos.action("del",d)
                safeprint(">>>> 退選 [" + str(d) + "] " + msg, color='green' if result else 'red')
            except Exception as e:
                safeprint(str(e))
    print()
    if len(adds):
        safeprint('\n========== 開始加選({}) =========='.format(len(adds)), color='yellow')
        for a in adds:
            try:
                result, msg, soup = elecos.action("add",a)
                safeprint(">>>> 加選 [" + str(a) + "] " + msg, color='green' if result else 'red')
            except Exception as e:
                safeprint(str(e))

    print_timetabe(soup)
    safeprint('\n========== 任務完成 程序結束 ==========', back='on_green')

if __name__ == '__main__':
    import configs as cfg
    from datetime import datetime

    fuck = lambda: fuck_elecos(cfg.student_no,cfg.password,cfg.adds,cfg.dels,cfg.try_times,cfg.login_interval)
    def wait_start(runTime, action):
        while runTime > datetime.now():
            time.sleep(cfg.schedule_interval)
        return action()

    start_time = datetime(*cfg.start_time)
    if start_time > datetime.now():
        safeprint('[#] 當前時間', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), color='cyan')
        safeprint('[!] 程式將在 {} 執行，請勿關閉程式。'.format(start_time.strftime("%Y-%m-%d %H:%M:%S")), color='yellow')
        wait_start(start_time, fuck)
    else:
        fuck()
