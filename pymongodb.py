from pymongo import MongoClient,ASCENDING
from config import mgconfig
from datetime import datetime

'''
conn = MongoClient('127.0.0.1', 27017)
db = conn.bbsdb
my_db = db.test_set
my_db.insert({"name":"jiayiming", "age":18})
'''
try:
    mongo = MongoClient(mgconfig['host'], mgconfig['port'])
    db = mongo[mgconfig.get('db_name')]
except Exception as e:
    print(e)


class Mongodb(object):

    __fileds__= [
        ('detele', bool, True)
    ]

    _instance = None
    _flag = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Mongodb, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self):
        if self.__class__._flag is None:
            self.set_name = db[self.__class__.__name__]
            self.id = self.set_name.find().count() + 1
            self.__class__._flag = 1


    @classmethod
    def new(cls, form, **kwargs):
        m = cls()
        for k, v in form.items():
            for filed in m.__fileds__:
                if k in filed:
                    try:
                        setattr(m, k, filed[1](v))
                    except:
                        setattr(m, k, filed[2])
                else:
                    if not hasattr(m , filed[0]):
                        setattr(m, filed[0],  filed[2])
        for k, v in kwargs.items():
            for filed in m.__fileds__:
                if k in filed:
                    try:
                        setattr(m, k, filed[1](v))
                    except:
                        setattr(m, k, filed[2])
        form = m.__dict__.copy()
        del form['set_name']
        m.set_name.insert(form)
        m.id += 1
        m.set_name.create_index([('id', ASCENDING)], unique=True)


    @classmethod
    def find_by(cls, **kwargs):
        m = cls()
        return m.set_name.find_one(kwargs)


    @classmethod
    def find_all(cls, **kwargs):
        m = cls()
        return list(m.set_name.find(kwargs))


    @classmethod
    def update(cls, id, **kwargs):
        m = cls()
        query = (
            {"id": id},
            {'$set': kwargs},
        )
        try:
            m.set_name.update(query[0], query[1])
        except Exception as e:
            print(e)


    @classmethod
    def delete(cls, id):
        try:
            cls.update(id, detele=False)
        except Exception as e:
            print(e)


    def __repr__(self):
        properties = ["({0}）:{1}".format(k, v) for k, v in self.__dict__.items()]
        return  " \n".join(properties)
