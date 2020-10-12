import json
import os
import typing
import dataclasses
from core import error
    
    
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 7776

    
@dataclasses.dataclass
class NetAddress(object):
    host: str
    port: int


def parse_dataclass(payload, keywords, Model):
    for keyword in keywords:
        if keyword not in payload:
            raise error.ConfigError("Config file is corrupted")
    args = (payload.get(keyword) for keyword in keywords)
    return Model(*args)


def parse_net_address(address) -> NetAddress:
    required_keywords = ['host', 'port']
    return parse_dataclass(address, required_keywords, NetAddress)


class Config(object):
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise error.ConfigError(f"Could not find configuration file: {path}")
        
        cfg = {}
        with open(path, 'r') as f:
            cfg = json.loads(f.read())
        
        self.load_api(cfg)
        self.load_services(cfg)

    def load_api(self, cfg):        
        if 'api' not in cfg:
            cfg['api'] = {}

        self.api = NetAddress(cfg['api'].get('host', DEFAULT_HOST), cfg['api'].get('port', DEFAULT_PORT))
      

    def load_services(self, cfg):
        if 'services' not in cfg:
            raise error.ConfigError("Config file is corrupted")

        services = cfg.get("services")

        if 'connector' not in services:
            raise error.ConfigError("Config file is corrupted")
        
        self.connector = parse_net_address(services.get('connector'))

