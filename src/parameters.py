from dataclasses import dataclass

@dataclass
class HestonParameters:
    v0: float
    theta: float
    kappa: float
    xi: float
    rho: float

