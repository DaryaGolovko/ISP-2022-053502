import myjson
import myyaml
import mytoml


class Creator:

    @staticmethod
    def create(inp: str):
        if inp == "json":
            return myjson.Json()

        elif inp == "yaml":
            return myyaml.Yaml()

        elif inp == "toml":
            return mytoml.Toml()
