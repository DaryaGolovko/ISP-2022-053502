import json_serializer
import json_deserializer


class Json:
    @staticmethod
    def dump(obj: object) -> str:
        return json_serializer.Serializer.dumps(obj)

    @staticmethod
    def load(s: str) -> object:
        return json_deserializer.Deserializer.loads(s)
