#!python3.8
import json
import sys

"""
递归从根任务节点，获取所有有子节点的任务
结果返回json

{
    "taskid": 1,
    "children": [
        {
            "taskid": 2,
            "children": [
                {
                    "taskid": 3,
                    "children": []
                },
                {
                    "taskid": 4,
                    "children": []
                },
                {
                    "taskid": 5,
                    "children": []
                }
            ]
        },
        {
            "taskid": 6,
            "children": [
                {
                    "taskid": 7,
                    "children": []
                },
                {
                    "taskid": 8,
                    "children": []
                },
                {
                    "taskid": 9,
                    "children": []
                }
            ]
        },
        {
            "taskid": 10,
            "children": [
                {
                    "taskid": 11,
                    "children": []
                },
                {
                    "taskid": 12,
                    "children": []
                },
                {
                    "taskid": 13,
                    "children": []
                },
                {
                    "taskid": 14,
                    "children": []
                },
                {
                    "taskid": 15,
                    "children": []
                }
            ]
        },
        {
            "taskid": 16,
            "children": [
                {
                    "taskid": 17,
                    "children": []
                },
                {
                    "taskid": 18,
                    "children": []
                },
                {
                    "taskid": 19,
                    "children": []
                }
            ]
        },
        {
            "taskid": 20,
            "children": [
                {
                    "taskid": 21,
                    "children": []
                },
                {
                    "taskid": 22,
                    "children": []
                },
                {
                    "taskid": 23,
                    "children": []
                }
            ]
        },
        {
            "taskid": 24,
            "children": [
                {
                    "taskid": 25,
                    "children": []
                },
                {
                    "taskid": 26,
                    "children": []
                },
                {
                    "taskid": 27,
                    "children": []
                }
            ]
        },
        {
            "taskid": 28,
            "children": [
                {
                    "taskid": 29,
                    "children": []
                },
                {
                    "taskid": 30,
                    "children": []
                },
                {
                    "taskid": 31,
                    "children": []
                }
            ]
        },
        {
            "taskid": 32,
            "children": [
                {
                    "taskid": 33,
                    "children": []
                },
                {
                    "taskid": 34,
                    "children": []
                },
                {
                    "taskid": 35,
                    "children": []
                },
                {
                    "taskid": 36,
                    "children": []
                }
            ]
        },
        {
            "taskid": 37,
            "children": [
                {
                    "taskid": 38,
                    "children": []
                },
                {
                    "taskid": 39,
                    "children": []
                }
            ]
        },
        {
            "taskid": 40,
            "children": [
                {
                    "taskid": 41,
                    "children": [
                        {
                            "taskid": 42,
                            "children": []
                        },
                        {
                            "taskid": 43,
                            "children": []
                        },
                        {
                            "taskid": 44,
                            "children": []
                        }
                    ]
                },
                {
                    "taskid": 45,
                    "children": [
                        {
                            "taskid": 46,
                            "children": []
                        },
                        {
                            "taskid": 47,
                            "children": []
                        }
                    ]
                },
                {
                    "taskid": 48,
                    "children": [
                        {
                            "taskid": 49,
                            "children": []
                        },
                        {
                            "taskid": 50,
                            "children": []
                        },
                        {
                            "taskid": 51,
                            "children": []
                        }
                    ]
                },
                {
                    "taskid": 52,
                    "children": [
                        {
                            "taskid": 53,
                            "children": []
                        },
                        {
                            "taskid": 54,
                            "children": []
                        }
                    ]
                },
                {
                    "taskid": 55,
                    "children": []
                }
            ]
        }
    ]
}

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

