"""
Pure Python Reverse-Mode Tape Automatic Differentiation Engine
Zero external dependencies.
"""
from autograd.tensor import Tensor
from autograd.nn import Linear, Sequential, Parameter
from autograd.optim import SGD, Adam
from autograd.attention import scaled_dot_product_attention, simulated_cuda_matmul

__all__ = [
    "Tensor",
    "Linear",
    "Sequential",
    "Parameter",
    "SGD",
    "Adam",
    "scaled_dot_product_attention",
    "simulated_cuda_matmul",
]
