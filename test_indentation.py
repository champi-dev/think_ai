"""Test file for indentation"""


class TestClass:
    def method1(self):
        if True:
            print("test")
            for i in range(10):
                print(i)
                if i > 5:
                    break
            else:
                print("else")

                def method2(self):
                    try:
                        x = 1
                        except BaseException:
                            pass
                    finally:
                        print("done")
