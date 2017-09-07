# -*- coding:utf-8 -*-

import os
import re
import csv
from textAnalysis import *
import databaseMethod

import sys
sys.path.append("..")
from config.config import *

class DOC(object):

    def __init__(self):
        self.docid = ""
        self.short_content = ""
        self.content_html = ""
        self.content_progress = ""

def get_amount(doc):
    defendant_list = get_defendant_name(doc)
    return

def get_defendant_new(doc):
    defendant=[]
    defendant_list=[]
    temp=re.findall('<div.*?>(.*?)</div>',doc.content_html,re.M)
    defendant_list=divide(temp,defendant_re)       
    defender_list=divide(temp,defender_re)
    suing_list=divide(temp,suing_re)
    zhikong_list=get_short_charge(temp,zhikong_re,zhikong_re_list)
    if suing_list!=[]:
        defendant_list=get_clear_defendant(defendant_list,suing_list[0],temp)
    if zhikong_list!=[]:
        defendant_list=get_clear_defendant(defendant_list,zhikong_list[0],temp)
    for j in range(0,len(defendant_list)):
        defendant.append(get_defendant(defendant_list[j]))
    defendant=get_final_defendant(defendant)
    return defendant

def get_defendant_name(doc):
    defendant_name = []
    for defendant in get_defendant_new(doc):
        defendant_name = defendant_name + [defendant[0]]
    print(defendant_name)
    return defendant

    

if __name__ == "__main__":
    database = 'wenshu_corruption'     #要连接的数据库
    sql = ''' SELECT docid, short_content, content_html,content_progress  FROM wenshu_corruption.t_anjian
                where content_progress='一审' or content_progress='二审' limit 10
        '''

    results = databaseMethod.data_get(userid,password,database,sql)
    docs = []
    for result in results:
        doc = DOC()
        doc.docid = result[0]
        doc.short_content = result[1]
        doc.content_html = result[2]
        doc.content_progress = result[3]        
        docs = docs + [doc]
        
    get_defendant_name(docs[0])
    #print(len(results))
    #print(results[0])
    #print(results[0][0])
    item = ['docid']
    info = []
    for doc in docs:
        info = info + [[doc.docid], get_defendant_name(doc)]
    print(info)
    write_csv("../temp/test_amount.csv", item, info)
    
    print("Get Amount: END")
