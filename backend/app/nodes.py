from typing import Dict, Any, List, Callable
import time


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


@register_node
class MultiplyNode(NodeBase):
    type = "multiply"

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
        result = a * b
        logs.append(f"{a} * {b} = {result}")
        context[node.get("id", "result")] = result

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(params.get("a"), (int, float)):
            errors.append("'a' must be a number")
        if not isinstance(params.get("b"), (int, float)):
            errors.append("'b' must be a number")
        return errors


@register_node
class ConditionNode(NodeBase):
    type = "condition"

    @classmethod
    def execute(
        cls,
        node: Dict[str, Any],
        logs: List[str],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        expr = params.get("expression", "")
        try:
            result = bool(eval(expr, {}, context))
        except Exception as e:
            result = False
            logs.append(f"Condition error: {e}")
        logs.append(f"{expr} -> {result}")
        context[node.get("id", "cond")] = result

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if "expression" not in params:
            return ["missing 'expression'"]
        return []


@register_node
class LoopNode(NodeBase):
    type = "loop"

    @classmethod
    def execute(
        cls,
        node: Dict[str, Any],
        logs: List[str],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        count = int(params.get("count", 1))
        for i in range(count):
            logs.append(f"loop {i + 1}/{count}")

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if not isinstance(params.get("count"), int) or params.get("count") < 1:
            return ["'count' must be a positive integer"]
        return []


@register_node
class DelayNode(NodeBase):
    type = "delay"

    @classmethod
    def execute(
        cls,
        node: Dict[str, Any],
        logs: List[str],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        ms = int(params.get("ms", 1000))
        logs.append(f"delay {ms}ms")
        time.sleep(ms / 1000.0)

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if not isinstance(params.get("ms"), int) or params.get("ms") < 0:
            return ["'ms' must be a non-negative integer"]
        return []
