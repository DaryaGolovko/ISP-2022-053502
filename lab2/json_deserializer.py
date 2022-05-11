import types
import marshal
import importlib
import inspect


class Deserializer:

    @staticmethod
    def deserialize_function(obj: dict) -> types.FunctionType:
        code: types.CodeType = marshal.loads(obj["code"].encode("cp437"))
        globs = Deserializer.deserialize_dict(obj["globals"])

        for i in obj["globals"]:
            if importlib.import_module(i) is not None:
                globs[i] = importlib.import_module(i)
                break

        return types.FunctionType(code, globs, obj["name"])

    @staticmethod
    def deserialize_class(obj: dict) -> type:
        return type(obj["name"], tuple(Deserializer.deserialize_list(obj["bases"])),
                    Deserializer.deserialize_dict(obj["attributes"]) and Deserializer.deserialize_dict(obj["methods"]))

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

        elif obj.get("type") is not None:
            if obj["type"] == "function":
                return Deserializer.deserialize_function(obj)

            if obj["type"] == "class":
                return Deserializer.deserialize_class(obj)

            if obj["type"] == "object":
                return Deserializer.deserialize_class_object(obj)
