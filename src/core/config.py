import json
import os
import typing
import dataclasses
from . import error
from .log import get_logger

log = get_logger("core.config")

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 7776


@dataclasses.dataclass
class NetAddress(object):
    host: str
    port: int


@dataclasses.dataclass
class DbData(object):
    host: str
    port: int
    name: str
    user: str


def parse_dataclass(payload, keywords, Model):
    for keyword in keywords:
        if keyword not in payload:
            log.warning(f"Config file is corrupted, cannot find {keyword}")
            raise error.ConfigError("Config file is corrupted")
    args = (payload.get(keyword) for keyword in keywords)
    return Model(*args)


def parse_net_address(address) -> NetAddress:
    required_keywords = ['host', 'port']
    return parse_dataclass(address, required_keywords, NetAddress)


def parse_db_data(data) -> DbData:
    required_keywords = ['host', 'port', 'name', 'user']
    return parse_dataclass(data, required_keywords, DbData)


class Config(object):
    def __init__(self, path: str):
        if not os.path.isfile(path):
            log.warning(f"Could not find configuration file: {path}")
            raise error.ConfigError(
                f"Could not find configuration file: {path}")

        cfg = {}
        with open(path, 'r') as f:
            cfg = json.loads(f.read())

        self.load_api(cfg)
        self.load_services(cfg)
        self.load_db(cfg)

    def load_db(self, cfg):
        if 'db' not in cfg:
            raise error.ConfigError("Cannot find db in config file")

        self.db = parse_db_data(cfg.get('db'))

    def load_api(self, cfg):
        if 'api' not in cfg:
            cfg['api'] = {}

        self.api = NetAddress(cfg['api'].get(
            'host', DEFAULT_HOST), cfg['api'].get('port', DEFAULT_PORT))

    def load_services(self, cfg):
        if 'services' not in cfg:
            log.warning("Could not find services in config file")
            raise error.ConfigError("Could not find services in config file")

        services = cfg.get("services")

        if 'connector' not in services:
            log.warning("Could not find connector service in config file")
            raise error.ConfigError(
                "Could not find connector service in config file")

        self.connector = parse_net_address(services.get('connector'))
