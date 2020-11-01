import enum


class ErrorCode(enum.IntEnum):
    INVALID_REQUEST = 1,
    CORRUPTED_PAYLOAD = 2,
    INVALID_CONFIG = 3,
    AGENT_NOT_EXIST = 100,
    INVALID_AGENT = 101,
    INVALID_HANDSHAKE = 200,
    CONNECTOR_ERROR = 201,
    CONNECTOR_RESPONSE_ERROR = 202,
    EVENT_ERROR = 500


class SparkleFatalError(Exception):
    def __init__(self, code: ErrorCode, description, name="SparkleFatalError"):
        super().__init__()
        self.code = code
        self.description = description
        self.name = name

    def __str__(self):
        return '<{}-{}/{}>'.format(self.name, self.code, self.description)


class SparkleError(SparkleFatalError):
    def __init__(self, code: ErrorCode, description, name="SparkleError"):
        super().__init__(code, description, name)


class ApiError(SparkleError):
    def __init__(self, code: ErrorCode, description):
        super().__init__(code, description, name="ApiError")


class ConnectorError(SparkleError):
    def __init__(self, code: ErrorCode, description):
        super().__init__(code, description, name="ConnectorError")


class ConnectorModelError(ConnectorError):
    pass


class EventError(SparkleError):
    def __init__(self, description):
        super().__init__(ErrorCode.EVENT_ERROR, description, name='EventError')


class ConfigError(SparkleError):
    def __init__(self, msg):
        super().__init__(ErrorCode.INVALID_CONFIG, msg, name='SparkleConfigError')
