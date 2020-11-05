import json
from pathlib import Path


config = {}


if __name__ == '__main__':
    exec(Path("config.py").read_text(), config)
    print(json.dumps(config["data"], indent=2))
