from han_secure_mqtt.models.response_code import ResponseCode

MessageStatesMap = {
    0: ResponseCode(code=0, message="INVALID"),
    1: ResponseCode(code=1, message="PUBLISH"),
    2: ResponseCode(code=2, message="WAIT_FOR_PUBACK"),
    3: ResponseCode(code=3, message="WAIT_FOR_PUBREC"),
    4: ResponseCode(code=4, message="RESEND_PUBREL"),
    5: ResponseCode(code=5, message="WAIT_FOR_PUBREL"),
    6: ResponseCode(code=6, message="RESEND_PUBCOMP"),
    7: ResponseCode(code=7, message="WAIT_FOR_PUBCOMP"),
    8: ResponseCode(code=8, message="SEND_PUBREC"),
    9: ResponseCode(code=9, message="QUEUED"),
}

MessageStatesMap[MessageStatesMap[0].message] = MessageStatesMap[0]
MessageStatesMap[MessageStatesMap[1].message] = MessageStatesMap[1]
MessageStatesMap[MessageStatesMap[2].message] = MessageStatesMap[2]
MessageStatesMap[MessageStatesMap[3].message] = MessageStatesMap[3]
MessageStatesMap[MessageStatesMap[4].message] = MessageStatesMap[4]
MessageStatesMap[MessageStatesMap[5].message] = MessageStatesMap[5]
MessageStatesMap[MessageStatesMap[6].message] = MessageStatesMap[6]
MessageStatesMap[MessageStatesMap[7].message] = MessageStatesMap[7]
MessageStatesMap[MessageStatesMap[8].message] = MessageStatesMap[8]
MessageStatesMap[MessageStatesMap[9].message] = MessageStatesMap[9]
