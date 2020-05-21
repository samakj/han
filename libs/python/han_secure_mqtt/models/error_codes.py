from han_secure_mqtt.models.response_code import ResponseCode


ErrorCodesMaps = {
    -1: ResponseCode(code=-1, message="AGAIN"),
    0: ResponseCode(code=0, message="SUCCESS"),
    1: ResponseCode(code=1, message="NOMEM"),
    2: ResponseCode(code=2, message="PROTOCOL"),
    3: ResponseCode(code=3, message="INVAL"),
    4: ResponseCode(code=4, message="NO_CONN"),
    5: ResponseCode(code=5, message="CONN_REFUSED"),
    6: ResponseCode(code=6, message="NOT_FOUND"),
    7: ResponseCode(code=7, message="CONN_LOST"),
    8: ResponseCode(code=8, message="TLS"),
    9: ResponseCode(code=9, message="PAYLOAD_SIZE"),
    10: ResponseCode(code=10, message="NOT_SUPPORTED"),
    11: ResponseCode(code=11, message="AUTH"),
    12: ResponseCode(code=12, message="ACL_DENIED"),
    13: ResponseCode(code=13, message="UNKNOWN"),
    14: ResponseCode(code=14, message="ERRNO"),
    15: ResponseCode(code=15, message="QUEUE_SIZE"),
}

ErrorCodesMaps[ErrorCodesMaps[-1].message] = ErrorCodesMaps[-1]
ErrorCodesMaps[ErrorCodesMaps[0].message] = ErrorCodesMaps[0]
ErrorCodesMaps[ErrorCodesMaps[1].message] = ErrorCodesMaps[1]
ErrorCodesMaps[ErrorCodesMaps[2].message] = ErrorCodesMaps[2]
ErrorCodesMaps[ErrorCodesMaps[3].message] = ErrorCodesMaps[3]
ErrorCodesMaps[ErrorCodesMaps[4].message] = ErrorCodesMaps[4]
ErrorCodesMaps[ErrorCodesMaps[5].message] = ErrorCodesMaps[5]
ErrorCodesMaps[ErrorCodesMaps[6].message] = ErrorCodesMaps[6]
ErrorCodesMaps[ErrorCodesMaps[7].message] = ErrorCodesMaps[7]
ErrorCodesMaps[ErrorCodesMaps[8].message] = ErrorCodesMaps[8]
ErrorCodesMaps[ErrorCodesMaps[9].message] = ErrorCodesMaps[9]
ErrorCodesMaps[ErrorCodesMaps[10].message] = ErrorCodesMaps[10]
ErrorCodesMaps[ErrorCodesMaps[11].message] = ErrorCodesMaps[11]
ErrorCodesMaps[ErrorCodesMaps[12].message] = ErrorCodesMaps[12]
ErrorCodesMaps[ErrorCodesMaps[13].message] = ErrorCodesMaps[13]
ErrorCodesMaps[ErrorCodesMaps[14].message] = ErrorCodesMaps[14]
ErrorCodesMaps[ErrorCodesMaps[15].message] = ErrorCodesMaps[15]
