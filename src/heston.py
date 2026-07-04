import numpy as np
from src.parameters import HestonParameters 

def characteristic_function(
        u: complex | float, #float?
        S: float,
        T: float,
        r: float,
        params: HestonParameters,
    ) -> complex:
    """
    Computes the Heston characteristic function φ(u).

    Parameters:
        u (complex | float): Integration variable.
        S (float): Current stock price.
        T (float): Time to expiry in years.
        r (float): Continuously compounded risk-free interest rate.
        params (HestonParameters): Heston model parameters.

    Returns:
        complex: The value of the characteristic function φ(u).
    """

    if u == 0:
        return 1 + 0j

    a = params.kappa * params.theta
    b = params.kappa
    d = (
        np.sqrt((params.rho * params.xi * 1j * u - b) ** 2 
        + params.xi**2 * (1j * u + u**2))
    )

    g_num = b - (params.rho*params.xi*1j*u) + d
    g_den = g_num - (2*d)
    g = g_num / g_den

    exp_dt = np.exp(d * T)
    C_first = 1j*r*T*u
    C_second = T*g_num - 2*np.log((1-g*exp_dt)/(1-g))
    C = C_first + (a/(params.xi**2))*C_second

    D_first = g_num / (params.xi**2)
    D_second = (1 - exp_dt) / (1 - g*exp_dt)
    D = D_first * D_second

    phi = np.exp(C + D*params.v0 + 1j*u*np.log(S))

    return phi
