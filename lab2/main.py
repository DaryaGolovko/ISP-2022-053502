import math
from factory import Creator


c = 42


def f(x):
    a = 123
    return math.sin(x * a * c)


class Human:
    @staticmethod
    def walk() -> str:
        return "mogu hodit"


with open(r'/Users/golovko/ISP-2022-053502/lab2/example.json', 'w') as file:
    s = Creator.create("json").dump(f)
    file.write(str(s))
    print(s)
    restored = Creator.create("json").load(s)
    print(restored(2))
