# Development workflow

Maintain the Schematics Retrieval Agent as one project on `main`.

- Work directly on `main` and push completed, validated changes to `origin/main`.
- Do not create development branches, separate project copies, or pull requests unless
  the user explicitly requests them.
- Fetch before pushing, preserve concurrent work, and never force-push `main`.
- Run the default test suite and `examples/quickstart.py` before pushing library changes.
- Keep the README focused on delivered functionality. Mark research extensions as planned
  until implemented and validated.
- Canonical store is the function graph + factor graph. USD is a projection.
- Do not import companion kernels. Do not invent edges. Do not clip refuses.
