"""Pinned companion SHAs. This package does not vendor those trees."""

JSPT = {
    "repo": "giasonpooni/Jacobian-Sensitivity-Propagation-Testbed",
    "sha": "f6e6296a35d632f01b626af617e3ba974402a356",
    "import": "sensitivity",
}

PLSR = {
    "repo": "giasonpooni/Parameterized-Lyapunov-Stability-Runtime",
    "sha": "9d0e7b4a1162e038150a71c63d986945d78135d4",
    "import": "lyapunov",
}

RCI = {
    "repo": "giasonpooni/Retrofitted-Computational-Instrumentation",
    "sha": None,
    "import": None,
}

CATALOGUE_ALIASES = {
    "jspt.reference.quadratic": "quadratic",
    "jspt.reference.exp2": "exp2",
    "jspt.reference.polar": "polar",
    "jspt.reference.affine2": "affine2",
    "jspt.reference.two-tank": "two-tank",
    "jspt.reference.beam-midspan": "beam-midspan",
}
