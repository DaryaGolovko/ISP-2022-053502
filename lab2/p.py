from importlib import import_module
import inspect
import Json
import marshal
import types
from typing import Dict, List


class MyPickle:
    @staticmethod
    def serialize_list(obj: List[any], _globals) -> List[any]:
        return [MyPickle.serialize(x) for x in obj]

    @staticmethod
    def serialize_dict(obj: Dict, _globals) -> Dict:
        res = {}
        for key, value in obj.items:
            res[key] = MyPickle.serialize(value, _globals)

        return res

    @staticmethod
    def serialize_func(obj: types.FunctionType, _globals) -> str:
        code: types.CodeType = obj.__code__
        code_string = str(marshal.dumps(code), "cp1252")

        name = obj.__name__

        used_imports: List[str] = []
        used_global_vars: Dict[str:any] = {}

        for key in code.co_names:
            value = _globals.get(key)
            if value is None:
                used_imports.append(key)
                continue

            if inspect.ismodule(value):
                _module: types.ModuleType = value
                used_imports.append(_module.__name__)
                continue

            if inspect.isfunction(value):
                continue

            used_global_vars[key] = MyPickle.serialize(value, _globals)

        res = {
            "__type__": "__func__",
            "name": name,
            "code": code_string,
            "imports": used_imports,
            "globals": used_global_vars,
        }
        return res

    @staticmethod
    def is_serializable_by_json(obj: object) -> bool:
        try:
            json.dumps(obj)
            return True
        except:
            return False

    @staticmethod
    def serialize_class(obj: type, _globals) -> object:
        supers = []
        for base in obj.__bases__:
            if base.__name__ != "object":
                supers.append(MyPickle.serialize_class(base, _globals))

        functions = inspect.getmembers(obj, predicate=inspect.isfunction)

        methods = {}
        for func in functions:
            methods[func[0]] = MyPickle.serialize_func(func[1], _globals)

        _attributes = inspect.getmembers(obj, predicate=lambda x: not inspect.isroutine(x))

        attributes = {}
        for attribute in _attributes:
            if attribute[0].startswith("__") and attribute[0].endswith("__"):
                continue

            attributes[attribute[0]] = MyPickle.serialize(attribute[1], _globals)

        name = obj.__name__
        res = {
            "__type__": "__class__",
            "name": name,
            "supers": supers,
            "methods": methods,
            "attributes": attributes,
        }

        return res

    @staticmethod
    def serialize_class_object(obj: object, _globals) -> object:
        attr = {}
        for key in dir(obj):
            if key.startswith("__") and key.endswith("__"):
                continue

            attribute = obj.__getattribute__(key)
            if inspect.ismethod(attribute):
                continue

            attr[key] = MyPickle.serialize(attribute, _globals)

        _class = MyPickle.serialize(obj.__class__, _globals)

        res = {
            "__type__": "__object__",
            "attributes": attr,
            "class": _class
        }

        return res

    @staticmethod
    def serialize(obj: object, _globals) -> object:
        if MyPickle.is_serializable_by_json(obj):
            return obj

        if inspect.isfunction(obj):
            return MyPickle.serialize_func(obj, _globals)

        if inspect.isclass(obj):
            return MyPickle.serialize_class(obj, _globals)

        if type(obj) is dict:
            return MyPickle.serialize_dict(obj, _globals)

        if type(obj) is list:
            return MyPickle.serialize_list(obj, _globals)

        if inspect.isclass(type(obj)):
            return MyPickle.serialize_class_object(obj, _globals)

        return "uWu ^-^"

    @staticmethod
    def deserialize_func(obj: object) -> types.FunctionType:
        name = obj["name"]
        code_string: str = obj["code"]
        code_string = code_string.encode("cp1252")
        code: types.CodeType = marshal.loads(code_string)
        imports = obj["imports"]
        _globals = obj["globals"]
        _globals = MyPickle.deserialize(_globals)

        for module_name in imports:
            try:
                _module = import_module(module_name)
                _globals[module_name] = _module
            except:
                pass

        res = types.FunctionType(code, _globals, name)
        return res

    @staticmethod
    def deserialize_class(obj: object) -> object:
        name = obj["name"]

        supers = obj["supers"]
        supers = MyPickle.deserialize(supers)

        methods = obj["methods"]
        methods = MyPickle.deserialize(methods)

        attributes = obj["attributes"]
        attributes = MyPickle.deserialize(attributes)

        res = type(name, tuple(supers), attributes | methods)
        return res

    @staticmethod
    def deserialize_class_object(obj: object) -> object:
        attributes = obj["attributes"]
        attributes = MyPickle.deserialize(attributes)

        _class = obj["class"]
        _class = MyPickle.deserialize(_class)

        res = _class.__new__(_class)
        for attribute in attributes.items():
            res.__setattr__(attribute[0], attribute[1])

        return res

    @staticmethod
    def deserialize(obj: object) -> object:
        if type(obj) is list:
            return [MyPickle.deserialize(x) for x in obj]

        if type(obj) is dict:
            if obj.get("__type__") != None:
                if obj["__type__"] == "__func__":
                    return MyPickle.deserialize_func(obj)

                if obj["__type__"] == "__class__":
                    return MyPickle.deserialize_class(obj)

                if obj["__type__"] == "__object__":
                    return MyPickle.deserialize_class_object(obj)

            res = {}
            for key, value in obj.items():
                res[key] = MyPickle.deserialize(value)

            return res

        if MyPickle.is_serializable_by_json(obj):
            return obj