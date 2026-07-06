from dataclasses import dataclass

@dataclass
class HestonParameters:
    v0: float
    theta: float
    kappa: float
    xi: float
    rho: float

def params_vector_to_params(params_vector):
    params = HestonParameters(
        v0 = params_vector[0],
        theta = params_vector[1],
        kappa = params_vector[2],
        xi = params_vector[3],
        rho = params_vector[4],
    )
    return params
