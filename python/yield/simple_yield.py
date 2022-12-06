# coding=utf-8
"""
yield == return + 生成器
内部next, 接着上一次结束的位置开始运行
"""


class TestYield(object):
    def __init__(self):
        pass

    def test_1(self):
        print("test_1 start...")

        while True:
            data = yield 1
            print("data:", data)

    def run_1(self):
        """
        yield 测试
        :return:
        """
        gene_1 = self.test_1()
        print("next(gene_1):", next(gene_1))
        print("-"*20)
        print("next(gene_1):", next(gene_1))

    def run_2(self):
        """
        yield send 测试
        :return:
        """
        gene_1 = self.test_1()
        print("next(gene_1):", next(gene_1))
        print("-" * 20)
        print("gene_1.send(2):", gene_1.send(2))

    def test_2(self, num):
        print("test_2 start...")

        while num < 10:
            num += 1
            yield num

    def run_3(self):
        """
        yield list 测试
        :return:
        """
        for data in self.test_2(0):
            print("data:", data)


if __name__ == '__main__':
    test = TestYield()
    # test.run_1()
    # test.run_2()
    test.run_3()