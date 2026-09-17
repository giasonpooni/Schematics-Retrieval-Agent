"""Write SAMPLED / REFUSED / UNRESOLVED onto the schematic. Never clip."""

from __future__ import annotations

from typing import Any, Mapping

from .eligibility import Decision
from .ir import EdgeKind, Node, NodeKind, Schematic, Status


def upsert_certificate(schematic: Schematic, *, node_id: str, owner: str, result: Status, target: str, edge: EdgeKind, attrs: Mapping[str, Any] | None = None) -> Node:
    payload = {"owner": owner, "result": result.value, **dict(attrs or {})}
    if node_id in schematic.nodes:
        node = Node(id=node_id, kind=NodeKind.CERTIFICATE, attrs=payload)
        schematic.replace(node)
    else:
        node = schematic.add(Node(id=node_id, kind=NodeKind.CERTIFICATE, attrs=payload))
        schematic.connect(edge, node_id, target)
    return node


def apply_decision(schematic: Schematic, decision: Decision, **extra: Any) -> Node | None:
    if decision.owner == "jspt" and decision.tool.startswith("jspt."):
        if decision.status is Status.ELIGIBLE:
            return None
        cert_id = f"cert:{decision.tool}:{decision.node_id}"
        result = Status.NOT_ELIGIBLE if decision.status is Status.NOT_ELIGIBLE else decision.status
        return upsert_certificate(schematic, node_id=cert_id, owner="jspt", result=result, target=decision.node_id, edge=EdgeKind.LINEARIZES, attrs={"reason": decision.reason, "tool": decision.tool, **extra})
    if decision.tool == "lyapunov.evaluate" and decision.status is Status.NOT_ELIGIBLE:
        return upsert_certificate(schematic, node_id=f"cert:lyapunov:{decision.node_id}", owner="plsr", result=Status.NOT_ELIGIBLE, target=decision.node_id, edge=EdgeKind.CERTIFIES, attrs={"reason": decision.reason, **extra})
    return None


def set_observer_status(schematic: Schematic, observer_id: str, status: Status, next_step: str) -> None:
    node = schematic.node(observer_id)
    attrs = dict(node.attrs)
    attrs["status"] = status.value
    attrs["next"] = next_step
    schematic.replace(Node(id=node.id, kind=node.kind, attrs=attrs))


def observer_next_step(schematic: Schematic) -> str:
    missing_digest = [n.id for n in schematic.of_kind(NodeKind.MEASUREMENT) if not n.get("rci_digest")]
    if missing_digest:
        return f"declare sensor quality or bind RCI digest on {missing_digest[0]}"
    no_A = True
    for n in schematic.of_kind(NodeKind.FUNCTION):
        for e in schematic.in_edges(n.id, EdgeKind.LINEARIZES):
            if schematic.node(e.src).get("result") == Status.SAMPLED.value:
                no_A = False
    if no_A:
        return "eligible JSPT call not yet sampled"
    return "observer mapped; no further declared gap"
