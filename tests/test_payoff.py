import numpy as np
from src.payoff import call_payoff

def test_call_payoff_scalar():
    assert call_payoff(150, 110) == 40
    assert call_payoff(90, 110) == 0
    assert call_payoff(110, 110) == 0

def test_call_payoff_array():
    S = np.array([90, 110, 150])
    K = 110
    result = call_payoff(S, K)
    expected = np.array([0, 0, 40])
    assert np.array_equal(result, expected)

