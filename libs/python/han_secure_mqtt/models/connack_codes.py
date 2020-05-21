from han_secure_mqtt.models.response_code import ResponseCode


ConnackCodesMap = {
    0: ResponseCode(code=0, message="ACCEPTED"),
    1: ResponseCode(code=1, message="BAD_PROTOCOL_VERSION"),
    2: ResponseCode(code=2, message="IDENTIFIER_REJECTED"),
    3: ResponseCode(code=3, message="SERVER_UNAVAILABLE"),
    4: ResponseCode(code=4, message="BAD_USERNAME_PASSWORD"),
}

ConnackCodesMap[ConnackCodesMap[0].message] = ConnackCodesMap[0]
ConnackCodesMap[ConnackCodesMap[1].message] = ConnackCodesMap[1]
ConnackCodesMap[ConnackCodesMap[2].message] = ConnackCodesMap[2]
ConnackCodesMap[ConnackCodesMap[3].message] = ConnackCodesMap[3]
ConnackCodesMap[ConnackCodesMap[4].message] = ConnackCodesMap[4]
