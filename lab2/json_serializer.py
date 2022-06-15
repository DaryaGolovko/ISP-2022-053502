import types
import inspect
import marshal


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
    def serialize_iterable(obj) -> dict:
        if type(obj) is dict:
            s = {}
            a = dict(obj)
            for i, j in a.items():
                s[i] = Serializer.dumps(j)
            return s
        elif type(obj) is set:
            s = set()
            for i in obj:
                s.add(Serializer.dumps(i))
            return s
        elif type(obj) is list:
            s = []
            for i in obj:
                s.append(Serializer.dumps(i))
            return s
        elif type(obj) is tuple:
            l = list()
            for i in obj:
                l.append(Serializer.dumps(i))
            s = tuple(l)
            return s

    @staticmethod
    def serialize_function(func: types.FunctionType) -> dict:
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
        code: types.CodeType = func.__code__
        code_string = str(marshal.dumps(code), "cp437")
        s = {"type": 'function',
             "name": func.__name__,
             "code": code_string,
             "globals": globs,
             "modules": libs
             }

        return s

    @staticmethod
    def serialize_class(obj) -> dict:
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

        return s

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

