import math
from factory import Creator

c = 2
l = [1, 2]
d = {"4": 2}


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
    assert (l == Creator.create("json").load(Creator.create("json").dump(l)))


def test_dict():
    assert (d == Creator.create("json").load(Creator.create("json").dump(d)))


def test_func():
    assert (foo == Creator.create("json").load(Creator.create("json").dump(foo)))


def test_class():
    man = Human()
    s = Creator.create("json").dump(man)
    restored_man = Creator.create("json").load(s)
    dubleman = restored_man()
    assert (man.walk == dubleman.walk)


if __name__ == "__main__":
    test_primitives()

    test_func()
    test_class()

    test_list()
    test_dict()

