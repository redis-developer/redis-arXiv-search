import os
from redisvl.schema import IndexSchema
from redisvl.index import AsyncSearchIndex


def get_index():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return IndexSchema.from_yaml(os.path.join(dir_path, "index.yaml"))


def get_async_index():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return AsyncSearchIndex.from_yaml(os.path.join(dir_path, "index.yaml"))
