#!python3.8
import json
import sys

"""
递归从根任务节点，获取所有有子节点的任务
结果返回json
"""

sys.path.append("/opt/midware/mpp_server/lib/python3.8/site-packages")
import mpxj
import jpype

jpype.startJVM()
from java.text import SimpleDateFormat
from net.sf.mpxj.reader import UniversalProjectReader
file = '/opt/data/mpp/tempfile.mpp'
project = UniversalProjectReader().read(file)

rootNode = project.getChildTasks()

print(rootNode)

print("rootNode len:", rootNode.size())


def geneInfo(rootNode):
    infodict = dict()
    curNode = rootNode[0].getChildTasks()
    infodict['taskid'] = curNode[0].getID()
    infodict['children'] = list()

    def recursionNode(curNode, infodict):
        # print("new re type: {}".format(type(curNode)))
        cursize = curNode.getChildTasks().size()
        if cursize <= 1:
            infodict['taskid'] = curNode.getID()
            infodict['children'] = list()
            return
        else:
            for task in curNode.getChildTasks():
                curdict = dict()
                curdict['taskid'] = task.getID()
                curdict['children'] = list()
                infodict['children'].append(curdict)
                recursionNode(task, curdict)

    recursionNode(curNode[0], infodict)
    print(json.dumps(infodict, indent=4))

# geneAllInfo(rootNode)
geneInfo(rootNode)

