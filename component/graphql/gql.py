# coding=utf-8
import sys
sys.path.append("/home/wgq/test/lib/python3.8/site-packages/")

import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(description='A typical hello world')

    def resolve_hello(self, info):
        return 'World'

schema = graphene.Schema(query=Query)


query = """
    query SayHello {
      hello
    }
"""
result = schema.execute(query)
print(result)

# ExecutionResult(data={'hello': 'World'}, errors=None)

