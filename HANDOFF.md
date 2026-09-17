# Handoff

v0.4.0 hangs local_structure on a function after a non-fixture sampled A.

Rules now enforced in code:

- Fixture A never opens PLSR or jspt.local_structure.
- rank and invisible are JSPT structure at x_star.
- They are not Kalman observability, identifiability, or a Lyapunov certificate.
- Missing sensitivity is NOT_CHECKED.

Still open:

1. Live sensitivity / lyapunov CI extra against the pinned SHAs.
2. Richer USDA compile from hand-authored scenes that are not SRA projections.
3. Field RCI records.
4. Optional first-order covariance when a Sigma is declared on the factor graph.

Do not start a search service.
