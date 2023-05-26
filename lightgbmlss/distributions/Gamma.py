from torch.distributions import Gamma as Gamma_Torch
from lightgbmlss.utils import *
from .distribution_utils import *


class Gamma:
    """
    Gamma distribution class.

     Distributional Parameters
    --------------------------
    concentration: torch.Tensor
        shape parameter of the distribution (often referred to as alpha)
    rate: torch.Tensor
        rate = 1 / scale of the distribution (often referred to as beta)

    Source
    -------------------------
    https://pytorch.org/docs/stable/distributions.html#gamma

    Parameters
    -------------------------
    stabilization: str
        Stabilization method for the Gradient and Hessian. Options are "None", "MAD", "L2".
    response_fn: str
        When a custom objective and metric are provided, LightGBM doesn't know its response and link function. Hence,
        the user is responsible for specifying the transformations. Options are "exp" or "softplus".
    """
    def __init__(self,
                 stabilization: str = "None",
                 response_fn: str = "exp"
                 ):
        # Check Response Function
        if response_fn == "exp":
            response_fn = exp_fn
            inverse_response_fn = log_fn
        elif response_fn == "softplus":
            response_fn = softplus_fn
            inverse_response_fn = softplusinv_fn
        else:
            raise ValueError("Invalid response function. Please choose from 'exp' or 'softplus'.")

        # Specify Response and Link Functions
        param_dict = {"concentration": response_fn, "rate": response_fn}
        param_dict_inv = {"concentration": inverse_response_fn, "rate": inverse_response_fn}
        distribution_arg_names = list(param_dict.keys())

        # Specify Distribution
        self.dist_class = DistributionClass(distribution=Gamma_Torch,
                                            univariate=True,
                                            discrete=False,
                                            n_dist_param=len(param_dict),
                                            stabilization=stabilization,
                                            param_dict=param_dict,
                                            param_dict_inv=param_dict_inv,
                                            distribution_arg_names=distribution_arg_names
                                            )