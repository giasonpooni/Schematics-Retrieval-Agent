"""Bind an RCI digest. Do not interpret the sample."""

from __future__ import annotations

from ..ir import Node, NodeKind, Schematic, Status
from ..kernels import KernelEvent


def bind_digest(schematic: Schematic, measurement_id: str, digest: str) -> KernelEvent:
    node = schematic.node(measurement_id)
    if node.kind is not NodeKind.MEASUREMENT:
        return KernelEvent(tool="rci.bind", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": f"{measurement_id} is {node.kind.value}, not a measurement"})
    if not digest or digest.startswith("interpret:"):
        return KernelEvent(tool="rci.bind", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": "digest empty or trying to smuggle an interpretation"})
    attrs = dict(node.attrs)
    attrs["rci_digest"] = digest
    if attrs.get("quality") == "undeclared":
        attrs["quality"] = "bound"
    schematic.replace(Node(id=node.id, kind=node.kind, attrs=attrs))
    return KernelEvent(tool="rci.bind", owner="rci", node_id=measurement_id, result=Status.SAMPLED, detail={"rci_digest": digest, "interpreted": False})
