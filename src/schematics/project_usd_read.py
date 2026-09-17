"""Read back a USDA this package emitted. Refuse incomplete schemas."""

from __future__ import annotations

import re

from .ir import EdgeKind, Node, NodeKind, Schematic
from .validate import require

_KIND = {k.value: k for k in NodeKind}
_EDGE = {k.value: k for k in EdgeKind}


def read_usda(text: str) -> Schematic:
    if "NsObservabilitySchematic@0.1" not in text:
        raise ValueError("UNRESOLVED: USDA is not an SRA projection (missing schema tag)")
    sch = Schematic(meta={"schema": "NsObservabilitySchematic@0.1", "source": "usda"})
    blocks = re.findall(r'def Scope "([^"]+)" \(\s*apiSchemas = \["([^"]+)"\]\s*\)\s*\{([^}]*)\}', text, flags=re.M)
    if not blocks:
        raise ValueError("UNRESOLVED: no Ns* prims with apiSchemas")
    for prim, api, body in blocks:
        kind_m = re.search(r'token ns:kind = "([^"]+)"', body)
        if not kind_m:
            raise ValueError(f"UNRESOLVED: {prim} missing ns:kind")
        kind = _KIND.get(kind_m.group(1))
        if kind is None:
            raise ValueError(f"UNRESOLVED: {prim} has unknown kind {kind_m.group(1)}")
        attrs: dict[str, object] = {}
        for key, raw in re.findall(r'(?:string|token) ns:([A-Za-z0-9_]+) = "([^"]*)"', body):
            if key != "kind":
                attrs[key] = raw
        for key, raw in re.findall(r"double ns:([A-Za-z0-9_]+) = ([0-9eE.+-]+)", body):
            attrs[key] = float(raw)
        for key, raw in re.findall(r"double\[\] ns:([A-Za-z0-9_]+) = \[([^\]]*)\]", body):
            attrs[key] = [float(p.strip()) for p in raw.split(",") if p.strip()]
        for key, raw in re.findall(r"bool ns:([A-Za-z0-9_]+) = ([01])", body):
            attrs[key] = raw == "1"
        node_id = "cert:" + prim[5:].replace("_", ":") if prim.startswith("cert_") else prim
        sch.add(Node(id=node_id, kind=kind, attrs=attrs))
    for kind_s, src, dst in re.findall(r'token ns:edge = "([^"]+)"\s+rel ns:src = </World/([^>]+)>\s+rel ns:dst = </World/([^>]+)>', text):
        edge = _EDGE.get(kind_s)
        if edge is None:
            raise ValueError(f"UNRESOLVED: unknown edge {kind_s}")
        src_id = "cert:" + src[5:].replace("_", ":") if src.startswith("cert_") else src
        dst_id = "cert:" + dst[5:].replace("_", ":") if dst.startswith("cert_") else dst
        if src_id not in sch.nodes or dst_id not in sch.nodes:
            raise ValueError(f"UNRESOLVED: edge {kind_s} {src}->{dst} missing endpoint")
        sch.connect(edge, src_id, dst_id)
    return require(sch)
