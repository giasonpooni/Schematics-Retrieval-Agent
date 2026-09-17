"""Bind an RCI digest or field record. Do not interpret the sample."""

from __future__ import annotations

from typing import Any

from ..ir import Node, NodeKind, Schematic, Status
from ..kernels import KernelEvent
from ..pins import RCI

CHAIN = ("board", "interface", "instrument", "installation")
QUALITY = ("acquisition", "timing", "calibration", "inference")
FORBIDDEN_QUALITY = {"GOOD", "good", "ok", "OK"}


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
    return KernelEvent(tool="rci.bind", owner="rci", node_id=measurement_id, result=Status.SAMPLED, detail={"rci_digest": digest, "interpreted": False, "pin": RCI})


def bind_record(schematic: Schematic, measurement_id: str, record: dict[str, Any]) -> KernelEvent:
    node = schematic.node(measurement_id)
    if node.kind is not NodeKind.MEASUREMENT:
        return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": f"{measurement_id} is not a measurement", "pin": RCI})
    if record.get("as_state") or record.get("promote_to_state"):
        return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": "refused promotion of a sample to a state", "pin": RCI})
    missing = [key for key in CHAIN if not str(record.get(key) or "").strip()]
    if missing:
        return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": f"incomplete chain: {missing}", "pin": RCI})
    quality = record.get("quality")
    if isinstance(quality, str) and quality in FORBIDDEN_QUALITY:
        return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": "one GOOD flag is forbidden", "pin": RCI})
    if not isinstance(quality, dict) or any(k not in quality for k in QUALITY):
        return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": f"quality must declare {list(QUALITY)}", "pin": RCI})
    if quality.get("inference") in {"observer updated", "predicted"}:
        return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.REFUSED, detail={"reason": "inference does not belong on the measurement record", "pin": RCI})
    attrs = dict(node.attrs)
    for key in CHAIN:
        attrs[key] = record[key]
    attrs["quality"] = {k: quality[k] for k in QUALITY}
    if record.get("rci_digest"):
        attrs["rci_digest"] = record["rci_digest"]
    if record.get("calibration"):
        attrs["calibration"] = record["calibration"]
    attrs["record_kind"] = "rci.field"
    schematic.replace(Node(id=node.id, kind=node.kind, attrs=attrs))
    return KernelEvent(tool="rci.bind_record", owner="rci", node_id=measurement_id, result=Status.SAMPLED, detail={"chain": list(CHAIN), "interpreted": False, "pin": RCI})
