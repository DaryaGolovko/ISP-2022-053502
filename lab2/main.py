import Json
import math

c = 2


def f():
    x = 2
    return math.sin(x)


class Cat:
    def __init__(self, name: str):
        self.name = name

    def pet(self) -> str:
        return "u pet a " + self.name


cat = Cat("l")
s = (2, 3)

print(Json.Serializer.dumps(cat))
