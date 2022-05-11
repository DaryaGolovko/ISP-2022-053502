import types
import inspect
import marshal
import importlib


class Serializer:

    @staticmethod
    def serialize_noniterable(obj: object):
        attr = {}

        for i in dir(obj):
            if not i.startswith("__") and not i.endswith("__"):
                attribute = obj.__getattribute__(i)
                if not inspect.ismethod(attribute):
                    attr[i] = Serializer.dumps(attribute)

        s = {"type": "object", "attr": attr, "class": obj.__class__}

        return str(s)

    @staticmethod
    def serialize_iterable(obj) -> str:
        if type(obj) is dict:
            s = {}
            a = dict(obj)
            for i, j in a.items():
                s[i] = Serializer.dumps(j)
            return str(s)
        elif type(obj) is set:
            s = set()
            for i in obj:
                s.add(Serializer.dumps(i))
            return str(s)
        elif type(obj) is list:
            s = []
            for i in obj:
                s.append(Serializer.dumps(i))
            return str(s)
        elif type(obj) is tuple:
            l = list()
            for i in obj:
                l.append(Serializer.dumps(i))
            s = tuple(l)
            return str(s)

    @staticmethod
    def serialize_function(func: types.FunctionType) -> str:
        libs = []
        globs = {}

        for i in func.__code__.co_names:
            if func.__globals__.get(i) is None:
                libs.append(i)

            elif inspect.ismodule(str(func.__globals__.get(i))):
                temp = types.ModuleType(func.__globals__.get(i))
                libs.append(temp.__name__)

            elif inspect.isfunction(i):
                continue

            globs[i] = Serializer.dumps(func.__globals__.get(i))

        s = {"type": 'function',
             "name": func.__name__,
             "code": str(marshal.dumps(func.__code__)),
             "globals": globs,
             "modules": libs
             }

        return str(s)

    @staticmethod
    def serialize_class(obj) -> str:
        methods = {}
        for func in inspect.getmembers(obj, predicate=inspect.isfunction):
            methods[func[0]] = Serializer.serialize_function(func[1])

        bases = []
        for i in obj.__bases__:
            if i.__name__ != "object":
                bases.append(Serializer.serialize_class(i))

        attr = {}
        for i in inspect.getmembers(obj, predicate=lambda x: not inspect.isroutine(x)):
            if not i[0].startswith("__") and i[0].endswith("__"):
                attr[i[0]] = Serializer.dumps(i[1])

        s = {"type": "class", "name": obj.__name__, "bases": bases, "methods": methods, "attributes": attr}

        return str(s)

    @staticmethod
    def dumps(obj):

        if type(obj) is int or type(obj) is float or type(obj) is bool or type(obj) is str:
            return obj

        elif inspect.isfunction(obj):
            return Serializer.serialize_function(obj)

        elif inspect.isclass(obj):
            return Serializer.serialize_class(obj)

        elif type(obj) is dict or type(obj) is tuple or type(obj) is set or type(obj) is list:
            return Serializer.serialize_iterable(obj)

        elif inspect.isclass(type(obj)):
            return Serializer.serialize_noniterable(obj)


class Deserializer:

    @staticmethod
    def deserialize_function(obj: dict) -> types.FunctionType:
        code: types.CodeType = marshal.loads(obj["code"].encode())
        globs = Deserializer.deserialize_dict(obj["globals"])

        for i in obj["libs"]:
            globs[i] = importlib.import_module(i)

        return types.FunctionType(code, globs, obj["name"])

    @staticmethod
    def deserialize_class(obj: dict) -> object:
        return type(obj["name"], tuple(Deserializer.deserialize_list(obj["bases"])),
                    Deserializer.deserialize_dict(obj["attributes"]) | Deserializer.deserialize_dict(obj["methods"]))

    @staticmethod
    def deserialize_class_object(obj: dict) -> object:
        s = Deserializer.loads(obj["class"]).__new__(type(Deserializer.deserialize_dict(obj["class"])))
        for i in Deserializer.deserialize_dict(obj["attributes"]).items():
            s.__setattr__(i[0], i[1])

        return s

    @staticmethod
    def deserialize_dict(obj: dict) -> dict or type:

        if obj.get("type") is not None:
            if obj["type"] == "function":
                return Deserializer.deserialize_function(obj)

            if obj["type"] == "class":
                return Deserializer.deserialize_class(obj)

            if obj["type"] == "object":
                return Deserializer.deserialize_class_object(obj)

        s = {}
        for key, value in obj.items():
            s[key] = Deserializer.loads(value)

        return dict(s)

    @staticmethod
    def deserialize_list(obj) -> list:
        s = []

        for i in obj:
            s.append(Deserializer.loads(i))

        return s

    @staticmethod
    def deserialize_set(obj) -> set:
        s = set()

        for i in obj:
            s.add(Deserializer.loads(i))

        return s

    @staticmethod
    def loads(obj) -> object:
        if type(obj) is int or type(obj) is float or type(obj) is bool or type(obj) is str:
            return obj

        elif type(obj) is list:
            return Deserializer.deserialize_list(obj)

        elif type(obj) is set:
            return Deserializer.deserialize_set(obj)

        elif type(obj) is dict:
            return Deserializer.deserialize_dict(obj)
