import logging
import toml
import os


class Dict(dict):
    __path__: list[str] = []

    def __init__(self, *args, path: list[str] = [], **kwargs):
        super().__init__(*args, **kwargs)
        self.__path__ = path

    def __getitem__(self, key: str):
        item = super().get(key, None)
        target_path = self.__path__ + [key]
        target_env = "_".join(target_path).upper()

        if not item:
            item = os.getenv(target_env, "")

        if isinstance(item, dict):
            item = Dict(item, path=target_path)

        if not item:
            logging.info(f"配置项 {target_env} 为空")

        return item


config = {
    "mysql": {
        "config": {
            "host": "127.0.0.1",
            "user": "root",
            "port": 3306,
            "password": "",
            "database": "",
        },
        "parameters": {
            "pool_size": 5,
            "charset": "utf8",
        },
    },
    "scheme": {
        "address": "0.0.0.0",
        "port": 8080,
    },
    "miniprogram": {
        "appid": "",
        "secret": "",
    },
}


CONFIG_FILEPATH = "config.toml"


def read_config() -> Dict:
    """ " 读取配置"""
    with open(CONFIG_FILEPATH, mode="r", encoding="utf-8") as f:
        config = toml.load(f)
    return Dict(config)


def write_config(config: Dict) -> None:
    """ " 写入配置"""
    with open(CONFIG_FILEPATH, mode="w", encoding="utf-8") as f:
        toml.dump(config, f)
    return None


try:
    config = read_config()
except FileNotFoundError:
    write_config(config)
    exit(f"请配置 {CONFIG_FILEPATH} 文件")
except Exception as e:
    exit(f"读取配置文件失败: {e}")
