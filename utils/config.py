import toml

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
    }
}


def read_config():
    """" 读取配置 """
    with open("config.toml") as toml_file:
        config = toml.load(toml_file)
    return config


def write_config(config):
    """" 写入配置 """
    with open("config.toml", 'w') as toml_file:
        toml.dump(config, toml_file)
    return None


try:
    config = read_config()
except FileNotFoundError:
    write_config(config)
    exit("请配置config.toml文件")
except Exception as e:
    exit(f"读取配置文件失败: {e}")
