from py2neo import Graph

'''
清空neo4j数据库所以节点与关系,非必要不调用
'''
class ClearGraph:
    def __init__(self):
        self.graph = Graph("http://0.0.0.0/:7474", auth=("neo4j", "neo4j"))
        print("开始清理")
        self.graph.run('match (n) detach delete n')
        print("清理完成")


if __name__ == '__main__':
    clear = ClearGraph()# 清空数据库
