# coding=utf-8
import csv

from os import environ
import pdb
from neo4j import *
import json

"""
TODO neo4j要求现有节点后有关系。然而is a关系的建立并不是这么个顺序。
"""


class DBOperator(object):
    def __init__(self):
        self._driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=("neo4j", "1234"))

    def close(self):
        self._driver.close()

    def findNodeIDByClassname(self,classname):
        with self._driver.session() as session:
            #pdb.set_trace()
            r = session.run("MATCH (n:BRMetaclass {classname: $classname}) RETURN n", classname=classname).single()
            if r:
                return r[0].id
            else:
                return None

    def connectNodes(self,fid,tid,reltype):
        with self._driver.session() as session:
            q = "MATCH (nf),(nt) WHERE ID(nf)={} AND ID(nt)={} CREATE (nf)-[r: {}]->(nt) RETURN r".format(fid,tid,reltype)
            r = session.run(q).single()
            if r:
                return r[0]
            else:
                return None


    def createNode(self,aClass):
        nodetype = aClass.__class__.__name__
        proplist = aClass.__dict__.items()
        s = ['{}:"{}"'.format(k,v) for (k,v) in proplist]
        properties = ",".join(s)
        print(nodetype)
        print(properties)

        with self._driver.session() as session:
            q = "CREATE (n:%s {%s} ) RETURN n" %(nodetype, properties)
            r = session.run(q).single()
            if r:
                return r[0].id
            else:
                return None

class BRClass(object):
    # 这个类一般没实例
    def __init__(self):
        do = DBOperator()
        self.__id = do.createNode(self)
        # 初始化时应该建立指向类型的连接
        
        classname = self.__class__.__name__
        print("classname: " + classname)
        
        # 根据自己类查找类的节点
        classnode_id = do.findNodeIDByClassname(classname)

        if classnode_id is not None:
             # link self.node to node[classname]
            do.connectNodes(self.__id,classnode_id,"A")
        else :
            raise Exception("%s:BRMetaclass not exist in neo4j yet. " % classname)

class BRMetaclass(BRClass):
    #classname should be unique
    # def createIndexAndConstraints on property
    def __init__(self, fromclass=None):
        print("BRMetaclass init")

        if fromclass is not None:
            self.classname = fromclass.__name__
            super(BRMetaclass,self).__init__()

class BRCountry(BRClass):
    
    def __init__(self,zhlabel,enlabel,comment,code2,code3,codenum):
        print("BRCountry init")
        self.zhlabel = zhlabel
        self.enlabel = enlabel
        self.comment= comment
        self.code2 = code2
        self.code3 = code3
        self.codenum = codenum
        super(BRCountry,self).__init__()
if __name__ == '__main__':
    

    # q = "MATCH (n) DELETE n"
    # db.cypher_query(q)

    # # init classes, and save them to neo4j
    # install_labels(BRMetaclass)
    # b1 = BRMetaclass(BRCountry)
    # b1.save()

    # install_labels(BRCountry)
    rlist = []
    with open("country_code.csv",encoding="utf-8") as f:
        country_reader = csv.reader(f)
        header = next(country_reader)
        for row in country_reader:
            rlist.append(row)
    BRMetaclass(BRMetaclass)
    r = BRMetaclass(BRCountry)
    node_list = [BRCountry(*item[1:]) for item in rlist]



    # r = []
    # with open("country_code.csv",encoding="utf-8") as f:
    #     country_reader = csv.reader(f)
    #     header = next(country_reader)
    #     for row in country_reader:
    #         r.append(row)

    # ct = BRCountry(*r[0][1:])
