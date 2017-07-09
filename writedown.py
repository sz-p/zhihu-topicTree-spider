#-*- coding: UTF-8 -*-
 
import sys  
import json
reload(sys)   
sys.setdefaultencoding('utf8') 
class Wd():
    def __init__(self, temporaryDataFileName, DataFileName):
        self.tdfn = temporaryDataFileName
        self.dfn = DataFileName
    def wd_temporaryData(self,jsonData):
        # pass
        file_object = open(self.tdfn,'a')
        for d in jsonData['msg'][1]:
            file_object.write(json.dumps(d[0][1],ensure_ascii=False, encoding="utf-8"))
            file_object.write(',')
            file_object.write(json.dumps(d[0][2],ensure_ascii=False, encoding="utf-8"))
            file_object.write('\n')
        file_object.close()
    def wd_Data(self,title,id,focus,parentsname,parentsid):
        file_object = open(self.dfn,'a')
        file_object.write('\n'+str(title)+','+str(id)+','+str(focus)+','+str(parentsname)+','+str(parentsid))
        file_object.close()



          