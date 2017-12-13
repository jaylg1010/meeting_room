#_author:"gang"
#date: 2017/12/13

class Base(object):
    def __init__(self,val):
        self.val=val

    def func(self):
        print(self.val)

class Foo(Base):
    def func(self):
        print(self.val,666)

class Bar(object):
    def __init__(self):
        self._registry={}

    def register(self,a,b=None):
        if not b:
            b = Base
        self._registry[a]=b(a)

b = Bar()
b.register(1,Foo)
b.register(2)

b._registry[1].func()
b._registry[2].func()
