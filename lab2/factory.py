import json_serializer
import myyaml
import mytoml


class Creator:

    @staticmethod
    def create_serializer(inp: str) -> object:
        if inp == "json":
            return json_serializer.Serializer()

        elif inp == "yaml":
            return myyaml.Yaml()

        elif inp == "toml":
            return mytoml.Toml()
