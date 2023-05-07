from sys import stdout
from logging import getLogger, StreamHandler
import yaml, hashlib
import logging

logger = getLogger(__name__)

def config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def read_yaml(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return data


def write_yaml_file(path, data):
    with open(path, 'w') as f:
        yaml.dump(data, f)


def hash_string(string):
    myhash = hashlib.sha1(string.encode('utf-8'))
    return myhash.hexdigest().upper()
