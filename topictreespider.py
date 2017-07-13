#-*- coding: UTF-8 -*-
import urllib2
import re
from pyquery import PyQuery as pq
import config
import time
from getsubtopic import Gst
from writedown import Wd
import random 
import sys
#根话题
# url = '/topic/19776749/organize/entire'
#可修改名称话题&&无子话题
#有子话题
# url = '/topic/19776751/organize/entire'

# 记录器
wd = Wd(config.tdfn,config.dfn)
# 获取子节点工具
gst = Gst()


global baseUrl
baseUrl = "https://www.zhihu.com"

# 抓取队列
global grabList
grabList = []

# 已抓取队列 用于判重
global haveList
haveList = {}

#获取页面内容
def get_html_value(url):
    try:
        request = urllib2.Request(url,headers=config.pageheaders)
        response = urllib2.urlopen(request)
        return response.read()
    except:
        return
# 获取关注人数
def get_topic_focus(htmlVlue):
    result = re.findall(".*<strong>(\d*)</strong>.*",htmlVlue)
    if(result):
        return result[0]
# 获取话题名称
def get_topic_title(htmlVlue):
    result = re.findall(".*<h1 class=\"zm-editable-content\"(\ ?.*)?>(.*)</h1>.*",htmlVlue)
    if(result):
        return result[0][1]
# 获取当前话题ID
def get_topic_id(url):
    result = re.findall(".*/topic/(\d*)/organize.*",url)
    if(result):
        return result[0]
# 获取父话题
def get_parents_str(htmlValue):
    d=pq(htmlValue)
    if(d):
        return d('.parent-topic')
# 获取父话题名称
def get_parents_title(parents_str):
    _list = []
    d = pq(parents_str)
    if(d):
        for i in range(0,len(d('a'))):
            _list.append(d('a').eq(i).html().encode('latin1').decode('utf8').strip())
        return _list
# 获取父话题ID
def get_parents_id(parents_str):
    _list = []
    d = pq(parents_str)
    if(d):
        for i in range(0,len(d('a'))):
            _list.append(d('a').eq(i).attr('data-token'))
        return _list
# 检查子话题数据
def check_subtopic_data(myjson,fatherid):
    # 检查数据是否正常
    if(isinstance(myjson, dict)):
        # 子话题是否获取完毕
        while(len(myjson['msg'][1])==11):
            wd.wd_temporaryData(myjson)
            url = 'https://www.zhihu.com/topic/'+fatherid+'/organize/entire?child='+myjson['msg'][1][10][0][2]+'&parent='+fatherid
            for i in range(0, len(myjson['msg'][1])-1):
                grabList.append(myjson['msg'][1][i][0][2])
            print '待 ' + str(len(grabList))
            sys.stdout.flush()
            time.sleep(config.sleeptime+random.uniform(0,3))
            myjson = gst.get_subtopic_json(url,config.subtopic_values,config.subtopic_headers)
        # 子话题获取完毕后
        wd.wd_temporaryData(myjson)            
        for i in range(0, len(myjson['msg'][1])):
            grabList.append(myjson['msg'][1][i][0][2])
        print '待 ' + str(len(grabList))
        sys.stdout.flush()
        return 'end'
    else:
        print "异常"
        print myjson
        sys.stdout.flush()
        time.sleep(60+random.uniform(0,3))
        return check_subtopic_data(myjson,fatherid)
# 检查抓取队列
def check_topiclist():
    if len(grabList)!=0:
        return 1
    else:
        return 0

# 获取一个话题数据
def getonetopic(url,topicid):
    initurl = str('https://www.zhihu.com/topic/'+str(topicid)+'/organize/entire?child='+str(topicid)+'&parent='+str(topicid))
    # 获取页面
    html = get_html_value(url)
    if(html!=None):
        # 获取父节点数据
        _parents_str = get_parents_str(html)
        # 记录话题树数据
        _title = get_topic_title(html)
        _id = get_topic_id(url)
        _focus = get_topic_focus(html)
        _parentsname = get_parents_title(_parents_str)
        _parentsid = get_parents_id(_parents_str)
        if(isinstance(_parentsname, list)):
            for i in range(0,len(_parentsname)):
                wd.wd_Data(_title,_id,_focus,_parentsname[i],_parentsid[i])
        else:
            wd.wd_Data(_title,_id,_focus,_parentsname,_parentsid)
        # 写入已抓取队列用于判重
        _url = get_topic_id(url)
        haveList[_url] = ''


# 程序入口
def starttopictreespider():  
    initID = 19776749
    initurl = baseUrl + '/topic/19776749/organize/entire#anchor-children-topic'
    # 获取话题数据
    getonetopic(initurl,initID)
    # 获取子话题数据
    subtopic_json = gst.get_subtopic_json(initurl,config.subtopic_values,config.subtopic_headers)
    # 检查子话题数据
    check_subtopic_data(subtopic_json,initID)

    # 检查抓取队列
    while(check_topiclist()):
        print '已 ' + str(len(haveList))
        print '待 ' + str(len(grabList))
        initurl = baseUrl + '/topic/'+grabList[0]+'/organize/entire#anchor-children-topic'
        initID = grabList[0]
        del grabList[0]
        if((initID in haveList)==False):
            sys.stdout.flush()
            time.sleep(config.sleeptime+random.uniform(0,3))
            getonetopic(initurl,initID)
            # 获取子节点数据
            subtopic_json = gst.get_subtopic_json(initurl,config.subtopic_values,config.subtopic_headers)
            # 检查子节点数据
            check_subtopic_data(subtopic_json,initID)
            
    print '抓取结束'

starttopictreespider()


