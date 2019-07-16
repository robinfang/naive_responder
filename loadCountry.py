# coding=utf-8
import csv
from neomodel import StructuredNode,StringProperty,RelationshipTo
from neomodel import config
from neomodel import install_labels
from neomodel import db
config.DATABASE_URL = 'bolt://neo4j:1234@localhost:7687' 


class BRMetaclass(StructuredNode):
    classname = StringProperty(unique_index=True, required=True)
    def __init__(self, fromclass=None, *args, **kwargs):
        if fromclass is not None:
            kwargs["classname"] = fromclass.__name__
        super(BRMetaclass, self).__init__(*args, **kwargs)

class BRClass(StructuredNode):
    # 这个类没实例
    is_a = RelationshipTo(BRMetaclass,'A')
    def __init__(self, *args, **kwargs):
        # 初始化时应该首先建立指向类型的连接
        # 获取代表自己实例所属的类对应的节点
        super(BRClass, self).__init__(*args, **kwargs)
        self.classnode = BRMetaclass.nodes.get_or_none(classname = self.__class__.__name__)
        print (self.__class__.__name__)
        if self.classnode is not None:
            #将实例的节点连接到类的节点
            self.save()
            self.is_a.connect(self.classnode)



class BRCountry(BRClass):
    zhlabel = StringProperty()
    enlabel = StringProperty()
    comment =StringProperty()
    code2 = StringProperty(unique_index=True, required=True)
    code3 = StringProperty()
    codenum = StringProperty()
    def __init__(self,zhlabel,enlabel,comment,code2,code3,codenum, *args, **kwargs):
        kwargs["zhlabel"] = zhlabel
        kwargs["enlabel"] = enlabel
        kwargs["comment"] = comment
        kwargs["code2"] = code2
        kwargs["code3"] = code3
        kwargs["codenum"] = codenum
        super(BRCountry,self).__init__(*args, **kwargs)

if __name__ == '__main__':
    
    # init classes, and save them to neo4j
    install_labels(BRMetaclass)
    b1 = BRMetaclass(BRCountry)
    b1.save()

    install_labels(BRCountry)
    r = []
    with open("country_code.csv",encoding="utf-8") as f:
        country_reader = csv.reader(f)
        header = next(country_reader)
        for row in country_reader:
            r.append(row)
            #r.append( BRCountry(*row[1:]) )
    #map(lambda x: x.save(), r)
    ct = BRCountry(*r[0][1:])
