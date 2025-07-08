from typing import Dict, Any, List, Callable, Awaitable
import asyncio


class NodeBase:
    type: str

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ) -> None:
        """Execute the node logic and optionally mutate the context."""
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
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        await log(params.get("message", ""))

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if "message" not in params:
            return ["missing 'message'"]
        return []


@register_node
class AddNode(NodeBase):
    type = "add"

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 0)
        result = a + b
        await log(f"{a} + {b} = {result}")
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
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 0)
        result = a * b
        await log(f"{a} * {b} = {result}")
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
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        expr = params.get("expression", "")
        try:
            result = bool(eval(expr, {}, context))
        except Exception as e:
            result = False
            await log(f"Condition error: {e}")
        await log(f"{expr} -> {result}")
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
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        count = int(params.get("count", 1))
        for i in range(count):
            await log(f"loop {i + 1}/{count}")

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if not isinstance(params.get("count"), int) or params.get("count") < 1:
            return ["'count' must be a positive integer"]
        return []


@register_node
class DelayNode(NodeBase):
    type = "delay"

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        ms = int(params.get("ms", 1000))
        await log(f"delay {ms}ms")
        await asyncio.sleep(ms / 1000.0)

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        if not isinstance(params.get("ms"), int) or params.get("ms") < 0:
            return ["'ms' must be a non-negative integer"]
        return []


@register_node
class SubtractNode(NodeBase):
    type = "subtract"

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 0)
        result = a - b
        await log(f"{a} - {b} = {result}")
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
class DivideNode(NodeBase):
    type = "divide"

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 1)
        if b == 0:
            await log("division by zero")
            result = None
        else:
            result = a / b
            await log(f"{a} / {b} = {result}")
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
class PowerNode(NodeBase):
    type = "power"

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 0)
        result = a ** b
        await log(f"{a} ** {b} = {result}")
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
class ModuloNode(NodeBase):
    type = "modulo"

    @classmethod
    async def execute(
        cls,
        node: Dict[str, Any],
        log: Callable[[str], Awaitable[None]],
        context: Dict[str, Any],
    ):
        params = node.get("params", {})
        a = params.get("a", 0)
        b = params.get("b", 1)
        if b == 0:
            await log("modulo by zero")
            result = None
        else:
            result = a % b
            await log(f"{a} % {b} = {result}")
        context[node.get("id", "result")] = result

    @classmethod
    def validate(cls, params: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(params.get("a"), (int, float)):
            errors.append("'a' must be a number")
        if not isinstance(params.get("b"), (int, float)):
            errors.append("'b' must be a number")
        return errors
