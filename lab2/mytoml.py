import toml
import json_serializer as ser
import json_deserializer as dser


class Toml:
    @staticmethod
    def dumps(obj: object) -> str:
        return toml.dumps(ser.Serializer.dumps(obj))

    @staticmethod
    def dump(obj: object, filepath: str,) -> None:
        with open(filepath, "w") as file:
            toml.dump(ser.Serializer.dumps(obj), file)

    @staticmethod
    def loads(s: str) -> object:
        return dser.Deserializer.loads(toml.loads(s))

    @staticmethod
    def load(filepath: str) -> object:
        with open(filepath, "r") as file:
            ser_obj = toml.load(file)

        return dser.Deserializer.loads(ser_obj)
