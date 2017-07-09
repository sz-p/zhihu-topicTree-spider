#-*- coding: UTF-8 -*-
import urllib2
import re
from pyquery import PyQuery as pq
import config
import time
from getsubtopic import Gct
from writedown import Wd
import random 
import sys
sys.stdout.flush()
#根话题W
# url = '/topic/19776749/organize/entire'
#可修改名称话题&&无子话题
#有子话题
# url = '/topic/19776751/organize/entire'
0

# 记录器
wd = Wd(config.tdfn,config.dfn)
# 获取子节点工具
gct = Gct()


#获取页面内容
def get_html_value(url):
    try:
        request = urllib2.Request(url,headers=config.mainheaders)
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
    d = pq(parents_str)
    if(d):
        return d('a').html().decode('utf8').strip()
# 获取父话题ID
def get_parents_id(parents_str):
    d = pq(parents_str)
    if(d):
        return d('a').attr('data-token')

def check_subtopic_data(myjson,fatherid):
    if(isinstance(myjson, dict)):
        while(len(myjson['msg'][1])==11):
            wd.wd_temporaryData(myjson)
            url = 'https://www.zhihu.com/topic/'+fatherid+'/organize/entire?child='+myjson['msg'][1][10][0][2]+'&parent='+fatherid
            for i in range(0, len(myjson['msg'][1])-1):
                grabList.append(myjson['msg'][1][i][0][2])
            print(len(grabList))
            sys.stdout.flush()
            time.sleep(config.sleeptime+random.uniform(0,3))
            myjson = gct.get_subtopic_json(url,config.subtopic_values,config.subtopic_headers)
        wd.wd_temporaryData(myjson)            
        for i in range(0, len(myjson['msg'][1])):
            grabList.append(myjson['msg'][1][i][0][2])
        print(len(grabList))
        sys.stdout.flush()
        return 'end'
    else:
        print "异常"
        print myjson
        sys.stdout.flush()
        time.sleep(60+random.uniform(0,3))
        return check_subtopic_data(myjson,fatherid)

def check_topiclist():
    if len(grabList)!=0:
        return 1
    else:
        return 0

# 抓取一层话题数据
def getonetopic(url,topicid):
    initurl = str('https://www.zhihu.com/topic/'+str(topicid)+'/organize/entire?child='+str(topicid)+'&parent='+str(topicid))
    # 获取页面
    html = get_html_value(url)
    if(html!=None):
        # 获取父节点数据
        parents_str = get_parents_str(html)

        print "话题名称 ",get_topic_title(html)
        print "话题ID ",get_topic_id(url)
        print "话题关注人数 ",get_topic_focus(html)
        print "父话题名称 ",get_parents_title(parents_str)
        print "父话题ID ",get_parents_id(parents_str)
        sys.stdout.flush()
        # 记录话题树数据
        wd.wd_Data(get_topic_title(html),get_topic_id(url),get_topic_focus(html),get_parents_title(parents_str),get_parents_id(parents_str))

global grabList
grabList = []
global baseUrl
baseUrl = "https://www.zhihu.com"

def starttopictreespider():  
    initID = 19776749
    initurl = baseUrl + '/topic/19776749/organize/entire#anchor-children-topic'
    # 获取话题数据
    getonetopic(initurl,initID)
    # 获取子话题数据
    subtopic_json = gct.get_subtopic_json(initurl,config.subtopic_values,config.subtopic_headers)
    # 检查子话题数据
    check_subtopic_data(subtopic_json,initID)

    # 检查抓取队列
    while(check_topiclist()):
        initurl = baseUrl + '/topic/'+grabList[0]+'/organize/entire#anchor-children-topic'
        initID = grabList[0]
        del grabList[0]
        print len(grabList)
        sys.stdout.flush()
        time.sleep(config.sleeptime+random.uniform(0,3))
        getonetopic(initurl,initID)
        # 获取子节点数据
        subtopic_json = gct.get_subtopic_json(initurl,config.subtopic_values,config.subtopic_headers)
        # 检查子节点数据
        check_subtopic_data(subtopic_json,initID)
            
    print '抓取结束'

starttopictreespider()


