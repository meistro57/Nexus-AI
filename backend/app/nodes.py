from typing import Dict, Any, List, Callable


class NodeBase:
    type: str

    @classmethod
    def execute(
        cls,
        node: Dict[str, Any],
        logs: List[str],
        context: Dict[str, Any],
    ):
        raise NotImplementedError

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        """Return list of validation error messages"""
        return []


NODE_REGISTRY: Dict[str, NodeBase] = {}


def register_node(node_cls: Callable):
    NODE_REGISTRY[node_cls.type] = node_cls
    return node_cls


@register_node
class PrintNode(NodeBase):
    type = "print"

    @classmethod
    def execute(
        cls,
        node: Dict[str, Any],
        logs: List[str],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        logs.append(params.get("message", ""))

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if "message" not in params:
            return ["missing 'message'"]
        return []


@register_node
class AddNode(NodeBase):
    type = "add"

    @classmethod
    def execute(
        cls,
        node: Dict[str, Any],
        logs: List[str],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 0)
        result = a + b
        logs.append(f"{a} + {b} = {result}")
        context[node.get("id", "result")] = result

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(params.get("a"), (int, float)):
            errors.append("'a' must be a number")
        if not isinstance(params.get("b"), (int, float)):
            errors.append("'b' must be a number")
        return errors
