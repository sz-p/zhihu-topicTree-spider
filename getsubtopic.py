#-*- coding: UTF-8 -*-

import urllib
import urllib2
import json

import config
from writedown import Wd

wd = Wd(config.tdfn,config.dfn)
class Gct():
    def get_subtopic_json(self,url,values,headers):
        retry_time = 5
        flag = False
        while not flag:           
            if retry_time == 0:
                return
            try:
                data = urllib.urlencode(values)
                request = urllib2.Request(url,data,headers)
                response = urllib2.urlopen(request,data=None,timeout=config.timeout)
                subtopic_json = json.loads(response.read(),encoding="utf-8")
                return subtopic_json
            except urllib2.URLError, e:
                if hasattr(e,"reason"):
                    print u"错误原因",e
                retry_time -= 1





