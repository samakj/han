from collections import defaultdict
from typing import Callable, List


class TopicBlueprint:
    def __init__(self, topic_prefix: str = ""):
        self.topic_prefix = topic_prefix
        self.topic_action_handlers: defaultdict = defaultdict(lambda: defaultdict(list))

    def add_topic_rule(self, rule: str, actions: List[str], handler: Callable):
        for action in actions:
            self.topic_action_handlers[f"{self.topic_prefix}{rule}"][action].append(handler)

    def topic(self, rule: str, actions: List[str]) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_topic_rule(rule=rule, actions=actions, handler=func)
            return func
        return decorator

    def add_child_blueprint(self, blueprint: 'TopicBlueprint') -> None:
        for topic in blueprint.topic_action_handlers:
            for action, handlers in blueprint.topic_action_handlers[topic]:
                self.topic_action_handlers[f"{self.topic_prefix}{topic}"][action].extend(handlers)

