from han_secure_mqtt.models.response_code import ResponseCode

ConnectionStatesMap = {
    0: ResponseCode(code=0, message="NEW"),
    1: ResponseCode(code=1, message="CONNECTED"),
    2: ResponseCode(code=2, message="DISCONNECTING"),
    3: ResponseCode(code=3, message="CONNECT_ASYNC"),
}

ConnectionStatesMap[ConnectionStatesMap[0].message] = ConnectionStatesMap[0]
ConnectionStatesMap[ConnectionStatesMap[1].message] = ConnectionStatesMap[1]
ConnectionStatesMap[ConnectionStatesMap[2].message] = ConnectionStatesMap[2]
ConnectionStatesMap[ConnectionStatesMap[3].message] = ConnectionStatesMap[3]
