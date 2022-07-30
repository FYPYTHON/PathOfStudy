# coding=utf-8
# auth: 1823218990@qq.com
# https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
"""
body = {
    "query":{
        "match_all":{}
    },
    "aggs":{                        # 聚合查询
        "min_age/max_age/sum_age/avg_age":{                 # 最小值的key
            "min/max/sum/avg":{                 # 最小
                "field":"age"       # 查询"age"的最小值
            }
        }
    }
}
"""
from datetime import datetime
from elasticsearch import Elasticsearch
TIME_FPRMATE_UTC = "%Y-%m-%dT%H:%M:%S.%fZ"
host = '127.0.0.1'
port = 9200
auth = ('root', '1234')
es = Elasticsearch([{"host": host, "port": port}]
                   , http_auth=auth
                   , timeout=3600
                   )

if es.ping():
    print("es is connect...")
else:
    print("es not connect...")
    es = None

default_index = 'systemprofile*'
full_index = "systemprofile_2019-07"
default_type = 'diskinfo'
default_id = "*"
key = 'min_cpu'
action = 'min'
field = 'cpu_per'
default_body = {
    "query": {
        "match_all": {}
    },
    "aggs": {                        # 聚合查询
        "%s" % key:{                 # 最小值的key
            "%s" % action: {                 # 最小
                "field": "%s" % field       # 查询"age"的最小值
            }
        }
    }
}


def es_create_index(index_name):
    res = es.indices.create(index=index_name)
    print(res)


def es_delete_index(index_name):
    res = es.indices.delete(index=index_name)
    print(res)


def es_add_data(index_name, doc_type, body, id=None):
    """
    from datetime import datetime
    data = {
        "@timestamp": datetime.now().strftime(TIME_FPRMATE_UTC)
        , "message": "testonly"
        , "user": "root"
        , "other": "..."
    }
    es_add_data('filebeat-2019.07.16', 'log', data, "1")
    :param index_name:
    :param doc_type:
    :param id:
    :param body:
    :return:
    """
    res = es.index(index=index_name, doc_type=doc_type, id=id, body=body)
    print(res)


def es_delete_data(index, doctype, id):
    """
    :param index:  full index
    :param doctype:
    :param id:
    :return:
    """
    res = es.delete(index=index, doc_type=doctype, id=id)
    print(res)


def es_delete_data_by_query(index, body):
    """
    eg:
    data = {
        "query": {
            "match": {
                "@timestamp": "2019-07-16T15:15:37.685460Z"
            }
        }
    }
    es_delete_data_by_query('es-test-*/log', data)
    :param index: filebeat-*
    :param body: {
                    "query": {
                        "match_all": {
                            "@timestamp": "2019-07-16T02:02:36.351Z"
                        }
                    }
                }
    :param doc_type: log
    :param q:
    :return:
    """
    # res = es.delete_by_query(index, body, q=q)
    import requests
    headers = {'Content-Type': 'application/json'}
    params = '{}'.format(body)

    url = "http://{}:{}/{}/_delete_by_query".format(host, port, index)
    params = str(params).replace("'", '"')
    print(params, url)
    res = requests.post(url, headers=headers, data=params)
    print(res.text)


def es_search(index, q=""):
    """
    eg: es_search(index='filebeat-*', q="_id:1")
    index - 索引名
    q     - 查询指定匹配 使用Lucene查询语法  q=cpu_per:8.2 //  _id:1
    from_ - 查询起始点  默认0
    doc_type - 文档类型
    size  - 指定查询条数 默认10
    field - 指定字段 逗号分隔
    sort  - 排序  字段：asc/desc
    body  - 使用Query DSL
    scroll - 滚动查询
    :return:
    """
    result = es.search(index=index
                       , q=q
                       , from_=0
                       , size=10
                       # , doc_type="diskinfo"
              )
    print(result)


def es_search_with_body(index_name, body, offset=0, size=10):
    """
    body = {
        "query":{
            "match_all":{}
        }
        ,"from":2    # 从第二条数据开始
        ,"size":4    # 获取4条数据
        ,"sort":
            {"@timestamp": {"order": "desc"}}
    }
    result = es_search_with_body('filebeat-*', body, 10, 100)
    for res in result['hits']['hits']:
    print(res["_source"]['@timestamp'])
    :return:
    """
    print(body)
    result = es.search(index=index_name
                       # , q="pretty"
                       , from_=offset
                       , size=size
                       , body=body
                       )
    print(result)



def es_get(index_name, doc_type,  doc_id):
    """
    :param index_name:  systemprofile_2019-07
    :param doc_type:    diskinfo
    :param doc_id:      4cId7GsBbne0wq9Y1Yue
    :return:
    """
    res = es.get(index=index_name, id=doc_id, doc_type=doc_type)
    print(res)


def es_get_source(index_name, doctype):
    res = es.get_source(index=index_name, doc_type=doctype, id='4cId7GsBbne0wq9Y1Yue')
    print(res)


def es_get_mapping(index_name, doctype):
    res = es.indices.get_mapping(index=index_name, doc_type=doctype)
    print(res)


def es_count(index_name, doctype, doc_id, body):
    res = es.count(index=index_name, doc_type=doctype)
    print(res)
    print(res['count'])


def es_indices_get():
    # res = es.indices.get()
    res = es.indices.get_settings()
    print(res)


def es_put_settings(index_name, doctype, body):
    # 修改设置
    index_name = 'es-test'
    body = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    }
    res = es.indices.put_settings(body, index=index_name)
    print(res)


def es_put_template(index_name=None, doctype=None, body=None):
    # es.indices.get_template('es-test')
    index_name = 'es-test'
    body = {

      "index_patterns": "es-test-*",
      "settings": {
        "index.number_of_shards": 3,
        "number_of_replicas": 1,
        "index.refresh_interval": "60s"
      },
      "version": 1
    }
    res = es.indices.put_template(index_name, body)
    print(res)


if __name__ == "__main__":
    pass
    # es_search("filebeat-*")
    # es_get(full_index, default_type,  '4cId7GsBbne0wq9Y1Yue')
    # es_search_with_body(default_index, default_body)
    # es_count(full_index, default_type, "", "")
    # es_get_source(full_index, default_type)
    # es_get_mapping(full_index, default_type)
    # print(es.indices.get(index=full_index))
    # print(es.indices.get_settings())
    # es_indices("", "", "")
    # es_create_index("es-test")
    # es_delete_index("filebeat-*")
    # es_put_template()
    # print(es.indices.get_template())
    # es_delete_data('filebeat-2019.07.16', "log", '1')
    data = {
        "query": {
            "match": {
                "@timestamp": "2019-07-16T15:15:37.685460Z"
            }
        }
    }
    es_delete_data_by_query('es-test-*/log', data)

    # datas = {
    #     "@timestamp": datetime.now().strftime(TIME_FPRMATE_UTC)
    #     , "message": "testonly"
    #     , "user": "root"
    #     , "other": "..."
    # }
    # es_add_data('es-test-16', 'log', datas)





