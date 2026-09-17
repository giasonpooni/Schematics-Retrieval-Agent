# Handoff

v0.5.0 adds first-order covariance when sigma_x is declared on the function.

Rules now enforced in code:

- Do not invent Sigma_x from units, sensor names, or USD proximity.
- Fixture A never opens covariance, structure, or PLSR.
- Sigma_y ~ J Sigma_x J^T is exact only for affine maps.
- Nonlinear maps inherit the first-order remainder. Monte Carlo stays in JSPT.

Still open:

1. Live sensitivity / lyapunov CI extra against the pinned SHAs.
2. Richer USDA compile from hand-authored scenes that are not SRA projections.
3. Field RCI records.
4. Optional Monte Carlo gap as a separate experiment flag, not a default.

Do not start a search service.
