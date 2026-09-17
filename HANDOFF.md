# Handoff

v0.6.0 adds field RCI records, an optional Monte Carlo flag, and a CI extra for pinned JSPT/PLSR.

Rules now enforced in code:

- Field records require board, interface, instrument, installation.
- Quality is four axes. One GOOD flag is refused.
- Inference does not live on the measurement record.
- Samples are not promoted to states.
- Monte Carlo is --mc-covariance, never a default Sigma_y.

Still open:

1. Make the kernels CI job required once extras install cleanly in uv.
2. Richer USDA compile from hand-authored scenes that are not SRA projections.
3. Live RCI package import if that repo grows a Python contract module.

Do not start a search service.
