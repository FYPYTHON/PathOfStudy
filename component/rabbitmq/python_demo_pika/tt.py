# coding=utf-8

class TestA(object):
    def __init__(self):
        self.connect = None
        self.name = None

    def gogo(self):
        print("gogo a...")


class TestB(object):
    def __init__(self):
        self.connect = None
        self.name = None

    def gogo(self):
        print("gogo b...")



if __name__ == "__main__":
    a = TestA()
    b = TestB()
    a.b = b
    print(a.name)
    print(a.b)
    a.b.gogo()