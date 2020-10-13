import enum


class ErrorCode(enum.IntEnum):
    INVALID_REQUEST = 1,
    INVALID_CONFIG = 2,
    AGENT_NOT_EXIST = 100,
    INVALID_HANDSHAKE = 200,
    CONNECTOR_CONNECTION_DOWN = 201,
    CONNECTOR_RESPONSE_ERROR = 202,
    CONNECTOR_DISCONNECT_ERROR = 203,


class SparkleFatalError(Exception):
    def __init__(self, code: ErrorCode, description, name="SparkleFatalError"):
        self.code = code
        self.description = description
        self.name = name

    def __str__(self):
        return '<{}-{}/{}>'.format(self.name, self.code, self.description)


class SparkleError(SparkleFatalError):
    def __init__(self, code: ErrorCode, description, name="SparkleError"):
        super().__init__(code, description, name)


class ControllerError(SparkleError):
    def __init__(self, code: ErrorCode, description):
        super().__init__(code, description, name="ControllerError")


class ConnectorError(SparkleError):
    def __init__(self, code: ErrorCode, description):
        super().__init__(code, description, name="ConnectorError")


class ConnectorModelError(ConnectorError):
    pass


class ConfigError(SparkleError):
    def __init__(self, msg):
        super().__init__(ErrorCode.INVALID_CONFIG, msg, name='SparkleConfigError')
