import requests as rq
from bs4 import BeautifulSoup as bs
from pprint import pprint

URL_QUERY_COURSES = "http://esquery.tku.edu.tw/acad/query_result.asp"
URL_QUERY_DEPTS = "http://esquery.tku.edu.tw/acad/query.asp"
WEEKDAYS = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'日':7}

def get_course(tr_data):
    c = Course(
            grade=int(tr_data[1]),
            no=tr_data[2].split('(')[0],
            subject=tr_data[3],
            term=int(tr_data[5]),
            classno=tr_data[6],
            group=tr_data[7],
            obligatory=(tr_data[8].strip()=='必'),
            credit=int(tr_data[9]),
            name=tr_data[11],
            desc=tr_data[12],
            teacher=tr_data[14].split(' ')[0].split('(')[0],
            classtime=get_classes(tr_data[15:]))
    return c

def parse_tr(tr):
    result = []
    tds = tr.findChildren('td')
    for i in range(len(tds)):
        text = tds[i].text.strip()
        if i == 11:
            parts = text.split('\u3000')
            if len(parts) >= 2:
                result.append(parts[0])
                result.append(parts[1])
            else:
                result.append(text.replace('\u3000',''))
                result.append('')
        else:
            result.append(text.replace('\u3000',''))
    return result

class AttrDict(dict):
    def __setattr__(self,key,value):
        self[key] = value

    def __getattr__(self,key):
        return self[key]

class Course(AttrDict):
    def __init__(self,grade,no,subject,name,term,desc,classno,group,credit,obligatory,teacher,classtime):
        self.no = no
        self.subject = subject
        self.grade = grade
        self.classno = classno
        self.desc = desc
        self.term = term
        self.group = group
        self.name = name
        self.credit = credit
        self.obligatory = obligatory
        self.teacher = teacher
        self.classtime = classtime
        self.has_lab = False

    def __iadd__(self,other):
        if not self.subject == other.subject:
            raise Exception('Cannot merge two course with different subject!')
        if not other.group == 'P' or self.group == 'P':
            raise Exception('You can only merge course with lab-course!')
        if self.no == '':
            self.no = other.no
        self.has_lab = True
        for ct in other.classtime:
            ct.lab = True
            self.classtime.append(ct)
        return self

class ClassTime(AttrDict):
    def __init__(self,week,lesson,room):
        self.week = week
        self.lesson = lesson
        self.room = room
        self.index = week*100 + lesson
        self.lab = False

def get_classes(classes):
    result = []
    for c in classes:
        if c == '':
            continue
        try:
            t = [x.replace(' ','') for x in c.split('/')]
            week = WEEKDAYS[t[0]]
            room = t[2]
            for lesson in t[1].split(','):
                result.append(ClassTime(week,int(lesson),room))
        except:
            pass
    return sorted(result,key=lambda x: x.index)

def query_dept_courses(depts,dept):
    return query_courses(dict(func='go',R1='1',depts=depts,sgn1='-',dept=dept,level='999'))

def query_other_courses(other,others):
    return query_courses(dict(func='go',R1='5',others=others,sgn2='-',other=other))

def query_courses(payload):
    r = rq.post(URL_QUERY_COURSES,payload)
    r.encoding = 'Big5'
    s = bs(r.text,"lxml")
    trs = s.findAll('table')[2].findChildren('tr')
    courses = []
    for i in range(len(trs)):
        tr = trs[i]
        tr_data = parse_tr(tr)
        try:
            if len(tr_data) != 0 and (tr_data[0] == '' or tr_data[0] == '--'):
                c = get_course(tr_data)
                if not c: continue
                if c.group == 'P':
                    courses[-1] += c
                else:
                    courses.append(c)
        except:
            pprint(tr_data)
            raise

    return courses

def get_dept_groups():
    r = rq.get(URL_QUERY_DEPTS)
    r.encoding = 'Big5'
    s = bs(r.text,"lxml")
    depts = [[x['value'],x.text,get_depts(x['value'])] for x in s.find(id='depts').findAll('option')]
    return depts

def get_depts(dept_group):
    r = rq.get(URL_QUERY_DEPTS,dict(R1='1',depts=dept_group))
    r.encoding = 'Big5'
    s = bs(r.text,"lxml")
    return [[x['value'],x.text] for x in s.find(id='dept').findAll('option')]

def get_other_groups():
    r = rq.get(URL_QUERY_DEPTS)
    r.encoding = 'Big5'
    s = bs(r.text,"lxml")
    depts = [[x['value'],x.text,get_others(x['value'])] for x in s.find(attrs={'name':'other'}).findAll('option')]
    return depts

def get_others(other_group):
    r = rq.get(URL_QUERY_DEPTS,dict(R1='5',other=other_group.encode('big5')))
    r.encoding = 'Big5'
    s = bs(r.text,"lxml")
    return [[x['value'],x.text] for x in s.find(attrs={'name':'others'}).findAll('option')]

def get_all_course(depts = None, others = None):
    if depts == None:
        depts = get_dept_groups()
    if others == None:
        others = get_other_groups()

    for group in others:
        for dept in group[2]:
            print(group[1],dept[1])
            courses = query_other_courses(group[0],dept[0])
            if len(dept) >= 3:
                dept[2] = courses
            dept.append(courses)
    for group in depts:
        for dept in group[2]:
            print(group[1],dept[1])
            courses = query_dept_courses(group[0],dept[0])
            if len(dept) >= 3:
                dept[2] = courses
            dept.append(courses)
    return depts + others
