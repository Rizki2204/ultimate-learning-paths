import math
import random
from autograd.tensor import Tensor

class Parameter(Tensor):
    def __init__(self, data):
        super().__init__(data, requires_grad=True)

class Module:
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def parameters(self):
        params = []
        for v in self.__dict__.values():
            if isinstance(v, Parameter):
                params.append(v)
            elif isinstance(v, Module):
                params.extend(v.parameters())
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, Module):
                        params.extend(item.parameters())
        return params

class Linear(Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        # Xavier initialization
        limit = math.sqrt(6.0 / (in_features + out_features))
        w_data = [[random.uniform(-limit, limit) for _ in range(out_features)] for _ in range(in_features)]
        self.weight = Parameter(w_data)

        if bias:
            b_data = [0.0] * out_features
            self.bias = Parameter(b_data)
        else:
            self.bias = None

    def forward(self, x):
        out = x.matmul(self.weight)
        if self.bias is not None:
            out = out + self.bias
        return out

class Sequential(Module):
    def __init__(self, *layers):
        super().__init__()
        self.layers = list(layers)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
