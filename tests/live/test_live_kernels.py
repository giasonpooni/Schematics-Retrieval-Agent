import pytest

from schematics import Status, quadratic_drag
from schematics.adapters.jspt import JsptUnavailable, call_jacobian_at, load_sensitivity
from schematics.adapters.plsr import PlsrUnavailable, load_lyapunov
from schematics.adapters.rci import RciUnavailable, load_instrument_chain
from schematics.pins import JSPT, PLSR, RCI

pytestmark = pytest.mark.live


def test_sensitivity_imports_at_pin():
    try:
        mod = load_sensitivity()
    except JsptUnavailable:
        pytest.skip("sensitivity not installed")
    assert hasattr(mod, "jacobian_at")
    assert JSPT["import"] == "sensitivity"


def test_lyapunov_imports_at_pin():
    try:
        mod = load_lyapunov()
    except PlsrUnavailable:
        pytest.skip("lyapunov not installed")
    assert hasattr(mod, "plant_from_jacobian")
    assert PLSR["import"] == "lyapunov"


def test_instrument_chain_imports_at_pin():
    try:
        mod = load_instrument_chain()
    except RciUnavailable:
        pytest.skip("instrument_chain not installed")
    assert hasattr(mod, "Quality")
    assert hasattr(mod, "Assembly")
    assert RCI["import"] == "instrument_chain"


def test_live_jacobian_samples_A():
    try:
        load_sensitivity()
    except JsptUnavailable:
        pytest.skip("sensitivity not installed")
    event = call_jacobian_at(quadratic_drag(), "f")
    assert event.result is Status.SAMPLED
