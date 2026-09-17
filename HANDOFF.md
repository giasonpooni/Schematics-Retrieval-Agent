# Handoff

v0.2.0 adds a pinned JSPT adapter, PLSR eligibility only on non-fixture A,
RCI digest bind, and a refuse-closed USDA reader for SRA projections.

Still open:

1. Live sensitivity run against the pinned SHA (CI extra, not a default dep).
2. PLSR adapter that evaluates V only when fixture=false and result=SAMPLED.
3. Richer USDA compile from hand-authored scenes that are not SRA projections.
4. Field RCI records. Current bind is a digest string only.

Do not start a search service.
