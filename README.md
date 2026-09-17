# Schematics Retrieval Agent

Function-graph plus factor-graph IR for setting up observers on declared
nonlinear plants. The agent retrieves typed subgraphs, applies an eligibility
table, and writes fail-closed annotations.

Short name **SRA**. The reusable library import is `schematics`.

OpenUSD is a projection. This package is not a twin platform and does not
import JSPT, PLSR, RCI, or CSE at module load.

The central question is:

> Given an authored schematic, which subgraphs may call which kernel —
> and what remains UNRESOLVED?

## Install and run

Python 3.12 or 3.13.

```bash
git clone https://github.com/giasonpooni/Schematics-Retrieval-Agent.git
cd Schematics-Retrieval-Agent
uv run --python 3.13 python examples/quickstart.py
uv run --python 3.13 python examples/unknown_plant.py
uv run --python 3.13 --with pytest pytest -q
```

CLI:

```bash
uv run --python 3.13 sra --fixture-A -o results
uv run --python 3.13 sra --call-jspt -o results
uv run --python 3.13 sra --rci-digest rci-displacement-digest-fixture -o results
```

`--call-jspt` wraps pinned `sensitivity` if that package is installed. It is not
a default dependency. A fixture A does not open PLSR.

Pin: `giasonpooni/Jacobian-Sensitivity-Propagation-Testbed@f6e6296a35d632f01b626af617e3ba974402a356`.

See [docs/KERNEL.md](docs/KERNEL.md), [docs/SCOPE.md](docs/SCOPE.md),
and [docs/MAP.md](docs/MAP.md).

## License

MIT. See [LICENSE](LICENSE).
