import unittest
import os
import json
import ddt
import pathlib
from core import config, error


TEST_CONFIG = f'{os.getenv("UTILS_PATH")}/test_config.json'
CORRUPTED_CONFIGS = [
    {},
    {
        'api': {}
    }, 
    {
        'api': {
            'host': 'localhost'
        }
    },
    {
        'api': {
            'port': 8000
        }
    },
    {
        'api': {
            'host': 'localhost',
            'port': 1111
        }
    },
    {
        'api': {
            'host': 'localhost',
            'port': 1111
        },
        'services': {

        }
    },
    {
        'api': {
            'host': 'localhost',
            'port': 1111
        },
        'services': {
            'connector': {

            }       
        }
    },
    {
        'api': {
            'host': 'localhost',
            'port': 1111
        },
        'services': {
            'connector': {
                'host': 'localhost'           
            }       
        }
    },
    {
        'api': {
            'host': 'localhost',
            'port': 1111
        },
        'services': {
            'connector': {
                'port': 1111,           
            }       
        }
    }
]


@ddt.ddt
class ConfigTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        if os.path.isfile(TEST_CONFIG):
            os.remove(TEST_CONFIG)
        super().setUp()
    
    def create_config_file(self, cfg):
        print(os.getcwd())
        print(TEST_CONFIG)
        filename = pathlib.Path(TEST_CONFIG)
        filename.touch(mode=0o777, exist_ok=True)            

        with open(filename, 'w+') as f:
            f.write(json.dumps(cfg))

    def test_read_config_from_invalid_path_expect_throw(self):
        self.assertRaises(error.ConfigError, lambda: config.Config("this_path_is_definitely_invalid"))


    @ddt.data(*CORRUPTED_CONFIGS)
    def test_read_corrupted_config_except_throw(self, cfg):
        self.create_config_file(cfg)
        self.assertRaises(error.ConfigError, lambda: config.Config(TEST_CONFIG))

    def test_read_valid_config_except_correct_fields(self):
        raw_cfg = {
            'api': {
                'host': 'localhost',
                'port': 1111
            },
            'services': {
                'connector': {
                    'port': 1111,
                    'host': 'localhost'           
                }       
            }
        }

        self.create_config_file(raw_cfg)
        cfg = config.Config(TEST_CONFIG)

        self.assertEqual(cfg.api.host, raw_cfg['api']['host'])
        self.assertEqual(cfg.api.port, raw_cfg['api']['port'])
        self.assertEqual(cfg.connector.host, raw_cfg['services']['connector']['host'])
        self.assertEqual(cfg.connector.port, raw_cfg['services']['connector']['port'])

    def test_read_config_without_api_keyword_expect_default_api_values(self):
        raw_cfg = {
            'services': {
                'connector': {
                    'port': 1111,
                    'host': 'localhost'           
                }       
            }
        }

        self.create_config_file(raw_cfg)
        cfg = config.Config(TEST_CONFIG)

        self.assertEqual(cfg.api.host, '0.0.0.0')
        self.assertEqual(cfg.api.port, 7776)
        self.assertEqual(cfg.connector.host, raw_cfg['services']['connector']['host'])
        self.assertEqual(cfg.connector.port, raw_cfg['services']['connector']['port'])
