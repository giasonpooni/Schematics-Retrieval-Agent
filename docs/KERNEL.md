# Kernel

This repository owns the schematic IR and eligibility routing.

It does not own A, V, samples, or dispositions.

| Object | Owner |
| --- | --- |
| Function graph, factor graph, typed edges | this repo |
| Address / type / path / blanket retrieval | this repo |
| Eligibility table | this repo |
| USD and mermaid projections | this repo (views) |
| `A = J`, chart law, local validity | JSPT (`sensitivity`) |
| Quadratic `V` | PLSR (`lyapunov`) |
| Qualified measurement record | RCI |
| SATISFIED / VIOLATED / UNRESOLVED | CSE |

Consumption is one way. Companion repos may pin a git SHA of this package.
This package does not import `sensitivity`, `lyapunov`, `gat`, or RCI.

A fixture `A` on the quadratic-drag example is tagged `fixture=true`.
It is not a JSPT sample. Replace it by wrapping `jacobian_at` in a later adapter.
