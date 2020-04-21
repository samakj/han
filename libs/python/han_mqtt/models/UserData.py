from dataclasses import dataclass


@dataclass
class MqttUserData:
    client_id: str
    username: str
    password: str

    @staticmethod
    def from_node_data(node_data: 'HanNodeData') -> 'MqttUserData':
        return MqttUserData(client_id=node_data.node_id, username=node_data.node_id, password=node_data.token)


@dataclass
class HanNodeData:
    node_id: str
    token: str

    @staticmethod
    def from_user_data(user_data: MqttUserData) -> 'HanNodeData':
        return HanNodeData(node_id=user_data.client_id, token=user_data.password)
