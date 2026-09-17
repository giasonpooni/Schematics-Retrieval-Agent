"""First-order covariance. Same J, second use. Do not invent Sigma_x."""

from __future__ import annotations

from typing import Any

from ..annotate import upsert_certificate
from ..eligibility import _written_A
from ..ir import EdgeKind, Schematic, Status
from ..kernels import KernelEvent
from ..pins import JSPT
from .jspt import JsptUnavailable, load_sensitivity


def declared_sigma(schematic: Schematic, function_id: str) -> list[list[float]] | None:
    raw = schematic.node(function_id).get("sigma_x")
    if raw is None:
        return None
    try:
        rows = [[float(v) for v in row] for row in raw]
    except TypeError:
        return None
    if not rows or any(len(row) != len(rows) for row in rows):
        return None
    return rows


def _matrix(value: Any) -> list[list[float]]:
    return [[float(v) for v in row] for row in value]


def call_first_order_covariance(schematic: Schematic, function_id: str) -> KernelEvent:
    cert_A = _written_A(schematic, function_id)
    sigma = declared_sigma(schematic, function_id)
    if cert_A is None or sigma is None:
        return KernelEvent(tool="jspt.first_order_covariance", owner="jspt", node_id=function_id, result=Status.NOT_ELIGIBLE, detail={"reason": "need non-fixture A and declared sigma_x", "pin": JSPT})
    A = cert_A.get("A")
    klass = schematic.node(function_id).get("class")
    try:
        sensitivity = load_sensitivity()
        pushed = sensitivity.first_order_covariance(A, sigma)
    except JsptUnavailable as exc:
        upsert_certificate(schematic, node_id=f"cert:jspt.cov:{function_id}", owner="jspt", result=Status.NOT_CHECKED, target=function_id, edge=EdgeKind.LINEARIZES, attrs={"tool": "jspt.first_order_covariance", "pin": f"{JSPT['repo']}@{JSPT['sha']}", "reason": str(exc)})
        return KernelEvent(tool="jspt.first_order_covariance", owner="jspt", node_id=function_id, result=Status.NOT_CHECKED, detail={"reason": str(exc), "pin": JSPT})
    except Exception as exc:
        upsert_certificate(schematic, node_id=f"cert:jspt.cov:{function_id}", owner="jspt", result=Status.REFUSED, target=function_id, edge=EdgeKind.LINEARIZES, attrs={"tool": "jspt.first_order_covariance", "sigma_x": sigma, "pin": f"{JSPT['repo']}@{JSPT['sha']}", "reason": str(exc)})
        return KernelEvent(tool="jspt.first_order_covariance", owner="jspt", node_id=function_id, result=Status.REFUSED, detail={"reason": str(exc), "pin": JSPT})
    upsert_certificate(
        schematic,
        node_id=f"cert:jspt.cov:{function_id}",
        owner="jspt",
        result=Status.SAMPLED,
        target=function_id,
        edge=EdgeKind.LINEARIZES,
        attrs={"tool": "jspt.first_order_covariance", "sigma_x": sigma, "sigma_y": _matrix(pushed), "exact_for_affine": klass == "linear", "pin": f"{JSPT['repo']}@{JSPT['sha']}", "reason": "Sigma_y ~ J Sigma_x J^T; remainder inherited for nonlinear maps"},
    )
    return KernelEvent(tool="jspt.first_order_covariance", owner="jspt", node_id=function_id, result=Status.SAMPLED, detail={"sigma_y": _matrix(pushed), "pin": JSPT})
