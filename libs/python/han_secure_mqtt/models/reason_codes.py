from han_secure_mqtt.models.response_code import ResponseCode

ReasonCodesMap = {
    0: ResponseCode(
        code=0,
        message="CLIENT_EXCEPTION",
        description="Client encountered an exception",
    ),
    1: ResponseCode(
        code=1,
        message="INVALID_PROTOCOL_VERSION",
        description="The protocol version requested is not supported by the server",
    ),
    2: ResponseCode(
        code=2,
        message="INVALID_CLIENT_ID",
        description="The server has rejected the supplied client ID",
    ),
    3: ResponseCode(
        code=3,
        message="BROKER_UNAVAILABLE",
        description="The broker is currently unavailable",
    ),
    4: ResponseCode(
        code=4,
        message="FAILED_AUTHENTICATION",
        description="Authentication with the server has failed, due to a bad username or password",
    ),
    5: ResponseCode(
        code=5,
        message="NOT_AUTHORIZED",
        description="Not authorized to perform the requested operation",
    ),
    6: ResponseCode(
        code=6,
        message="UNEXPECTED_ERROR",
        description="An unexpected error has occurred",
    ),
    32000: ResponseCode(
        code=32000,
        message="CLIENT_TIMEOUT",
        description="Client timed out while waiting for a response from the server",
    ),
    32001: ResponseCode(
        code=32001,
        message="NO_MESSAGE_IDS_AVAILABLE",
        description="Internal error, caused by no new message IDs being available",
    ),
    32100: ResponseCode(
        code=32100,
        message="CLIENT_ALREADY_CONNECTED",
        description="The client is already connected",
    ),
    32101: ResponseCode(
        code=32101,
        message="CLIENT_ALREADY_DISCONNECTED",
        description="The client is already disconnected",
    ),
    32102: ResponseCode(
        code=32102,
        message="CLIENT_DISCONNECTING",
        description="The client is currently disconnecting and cannot accept any new work",
    ),
    32103: ResponseCode(
        code=32103,
        message="SERVER_CONNECT_ERROR",
        description="Unable to connect to server",
    ),
    32104: ResponseCode(
        code=32104,
        message="CLIENT_NOT_CONNECTED",
        description="The client is not connected to the server",
    ),
    32105: ResponseCode(
        code=32105,
        message="SOCKET_FACTORY_MISMATCH",
        description="Server URI and supplied SocketFactory do not match",
    ),
    32106: ResponseCode(
        code=32106,
        message="SSL_CONFIG_ERROR",
        description="SSL configuration error",
    ),
    32107: ResponseCode(
        code=32107,
        message="CLIENT_DISCONNECT_PROHIBITED",
        description="MqttClient.disconnect call made from within a method on MqttCallback",
    ),
}

ReasonCodesMap[ReasonCodesMap[0].message] = ReasonCodesMap[0]
ReasonCodesMap[ReasonCodesMap[1].message] = ReasonCodesMap[1]
ReasonCodesMap[ReasonCodesMap[2].message] = ReasonCodesMap[2]
ReasonCodesMap[ReasonCodesMap[3].message] = ReasonCodesMap[3]
ReasonCodesMap[ReasonCodesMap[4].message] = ReasonCodesMap[4]
ReasonCodesMap[ReasonCodesMap[5].message] = ReasonCodesMap[5]
ReasonCodesMap[ReasonCodesMap[6].message] = ReasonCodesMap[6]
ReasonCodesMap[ReasonCodesMap[32000].message] = ReasonCodesMap[32000]
ReasonCodesMap[ReasonCodesMap[32001].message] = ReasonCodesMap[32001]
ReasonCodesMap[ReasonCodesMap[32100].message] = ReasonCodesMap[32100]
ReasonCodesMap[ReasonCodesMap[32101].message] = ReasonCodesMap[32101]
ReasonCodesMap[ReasonCodesMap[32102].message] = ReasonCodesMap[32102]
ReasonCodesMap[ReasonCodesMap[32103].message] = ReasonCodesMap[32103]
ReasonCodesMap[ReasonCodesMap[32104].message] = ReasonCodesMap[32104]
ReasonCodesMap[ReasonCodesMap[32105].message] = ReasonCodesMap[32105]
ReasonCodesMap[ReasonCodesMap[32106].message] = ReasonCodesMap[32106]
ReasonCodesMap[ReasonCodesMap[32107].message] = ReasonCodesMap[32107]
