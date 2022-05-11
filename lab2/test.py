import unittest
import math
from factory import Creator

c = 2
l = [1, 2]
d = {4: 2}


def foo():
    a = 3
    return math.sin(c + a)


class Human:
    @staticmethod
    def walk() -> str:
        return "mogu hodit"


def test_primitives():
    assert (c == Creator.create("json").load(Creator.create("json").dump(c)))


def test_list():
    print(l)
    print(Creator.create("json").load(Creator.create("json").dump(l)))
    assert (l == Creator.create("json").load(Creator.create("json").dump(l)))


def test_dict():
    s = Creator.create("json").dump(d)
    ser = Creator.create("json").load(s)

    assert (d == ser)


def test_func():
    s = Creator.create("json").dump(foo)
    ser = Creator.create("json").load(s)

    assert (foo() == ser())


def test_class():
    man = Human()
    s = Creator.create("json").dumps(man)
    restored_man = Creator.create("json").loads(s)

    dubleman = restored_man()

    assert (man.walk() == dubleman.walk())


if __name__ == "__main__":
    test_primitives()
    test_list()
    test_dict()


    test_func()
    test_class()
    unittest.main()
