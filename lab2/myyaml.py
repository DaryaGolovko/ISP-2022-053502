import yaml
import json_serializer as ser
import json_deserializer as dser


class Yaml:

    @staticmethod
    def dump(obj: object, filepath: str,) -> None:
        with open(filepath, "w") as file:
            yaml.dump(ser.Serializer.dumps(obj), file)

    @staticmethod
    def load(filepath: str) -> object:
        with open(filepath, "r") as file:
            ser_obj = yaml.load(file)
        return dser.Deserializer.loads(ser_obj)
