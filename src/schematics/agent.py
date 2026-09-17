"""Compile, retrieve, authorize, annotate. No architecture discovery in prose."""

from __future__ import annotations

from dataclasses import dataclass, field

from .adapters.jspt import call_coordinate_consistency, call_jacobian_at, call_perturbation_sweep
from .adapters.plsr import call_evaluate
from .adapters.rci import bind_digest
from .annotate import apply_decision, observer_next_step, set_observer_status
from .eligibility import Decision, decide
from .ir import NodeKind, Schematic, Status
from .kernels import KernelEvent, attach_fixture_linearization, plan
from .retrieve import blanket, by_kind
from .validate import require


@dataclass
class AgentReport:
    schematic: Schematic
    decisions: list[Decision]
    events: list[KernelEvent]
    blankets: dict[str, list[str]] = field(default_factory=dict)
    next_step: str = ""


def _drop_stale_lyapunov(schematic: Schematic, function_id: str) -> None:
    stale = f"cert:lyapunov:{function_id}"
    if stale in schematic.nodes and schematic.node(stale).get("result") == Status.NOT_ELIGIBLE.value:
        del schematic.nodes[stale]
        schematic.edges = [e for e in schematic.edges if e.src != stale and e.dst != stale]


def run(schematic: Schematic, *, attach_fixture_A: bool = False, call_jspt: bool = False, call_plsr: bool = False, rci_digest: str | None = None) -> AgentReport:
    require(schematic)
    decisions = decide(schematic)
    events = plan(decisions)
    for decision in decisions:
        apply_decision(schematic, decision)
    if rci_digest:
        for node in by_kind(schematic, NodeKind.MEASUREMENT):
            events.append(bind_digest(schematic, node.id, rci_digest))
    if attach_fixture_A:
        for node in by_kind(schematic, NodeKind.FUNCTION):
            if node.get("model_ref") == "jspt.reference.quadratic_drag":
                from .fixtures import fixture_A_at_xstar
                c = float(node.get("c", 0.5))
                x_star = float(node.get("x_star")[0])
                events.append(attach_fixture_linearization(schematic, node.id, A=fixture_A_at_xstar(c, x_star), validity_radius=0.02))
    if call_jspt:
        for decision in decide(schematic):
            if decision.tool == "jspt.jacobian_at" and decision.status is Status.ELIGIBLE:
                events.append(call_jacobian_at(schematic, decision.node_id))
            if decision.tool == "jspt.sweep_perturbation_scale" and decision.status is Status.ELIGIBLE:
                events.append(call_perturbation_sweep(schematic, decision.node_id))
            if decision.tool == "jspt.check_coordinate_consistency" and decision.status is Status.ELIGIBLE:
                events.append(call_coordinate_consistency(schematic, decision.node_id))
        for node in by_kind(schematic, NodeKind.FUNCTION):
            cert = f"cert:jspt:{node.id}"
            if cert in schematic.nodes and schematic.node(cert).get("fixture") is False:
                if schematic.node(cert).get("result") == Status.SAMPLED.value:
                    _drop_stale_lyapunov(schematic, node.id)
    if call_plsr:
        for decision in decide(schematic):
            if decision.tool == "lyapunov.evaluate" and decision.status is Status.ELIGIBLE:
                events.append(call_evaluate(schematic, decision.node_id))
    decisions = decide(schematic)
    blankets = {n.id: blanket(schematic, n.id) for n in by_kind(schematic, NodeKind.VARIABLE)}
    next_step = observer_next_step(schematic)
    status = Status.UNRESOLVED if any(n.kind is NodeKind.FUNCTION and n.get("class") == "unknown" for n in schematic.nodes.values()) else Status.MAPPED
    for obs in by_kind(schematic, NodeKind.OBSERVER):
        set_observer_status(schematic, obs.id, status, next_step)
    return AgentReport(schematic=schematic, decisions=decisions, events=events, blankets=blankets, next_step=next_step)
