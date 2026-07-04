from src.heston import characteristic_function
from src.parameters import HestonParameters
import pytest

DEFAULT_PARAMS = HestonParameters(
    v0 = 0.04,
    theta = 0.04,
    kappa = 2,
    xi = 0.3,
    rho = -0.7,
)

def test_characteristic_func_at_zero():
    u = 0
    S = 100
    T = 1
    r = 0.05
    phi = characteristic_function(u, S, T, r, DEFAULT_PARAMS)

    assert 1 == pytest.approx(phi)

def test_characteristic_func_is_complex():
    u = 1
    S = 100
    T = 1
    r = 0.05
    phi = characteristic_function(u, S, T, r, DEFAULT_PARAMS)

    assert isinstance(phi, complex)