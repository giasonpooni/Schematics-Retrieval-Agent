# Handoff

v0.3.0 adds a pinned PLSR adapter and a coordinate-consistency gate.

Rules now enforced in code:

- Fixture A never opens lyapunov.evaluate.
- PLSR takes A as an array through plant_from_jacobian. It does not form J.
- Missing lyapunov is NOT_CHECKED, not a certificate.
- jspt.check_coordinate_consistency is eligible only when a non-identity chart declares chart_T and chart_S.

Still open:

1. Live sensitivity / lyapunov CI extra against the pinned SHAs.
2. Hang local_structure (rank / ker J) on the function node after A.
3. Richer USDA compile from hand-authored scenes that are not SRA projections.
4. Field RCI records.

Do not start a search service.
