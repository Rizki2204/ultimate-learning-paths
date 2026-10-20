import math
from autograd.ops import zeros, shape

class Optimizer:
    def __init__(self, parameters):
        self.parameters = list(parameters)

    def zero_grad(self):
        for p in self.parameters:
            p.zero_grad()

    def step(self):
        raise NotImplementedError

class SGD(Optimizer):
    def __init__(self, parameters, lr=0.01, momentum=0.0):
        super().__init__(parameters)
        self.lr = lr
        self.momentum = momentum
        self.velocities = [zeros(p.shape) for p in self.parameters]

    def step(self):
        for p, v in zip(self.parameters, self.velocities):
            if p.grad is None:
                continue
            s = p.shape
            if len(s) == 1:
                for i in range(s[0]):
                    v[i] = self.momentum * v[i] + p.grad[i]
                    p.data[i] -= self.lr * v[i]
            elif len(s) == 2:
                for i in range(s[0]):
                    for j in range(s[1]):
                        v[i][j] = self.momentum * v[i][j] + p.grad[i][j]
                        p.data[i][j] -= self.lr * v[i][j]

class Adam(Optimizer):
    def __init__(self, parameters, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        super().__init__(parameters)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [zeros(p.shape) for p in self.parameters]
        self.v = [zeros(p.shape) for p in self.parameters]

    def step(self):
        self.t += 1
        lr_t = self.lr * math.sqrt(1.0 - self.beta2 ** self.t) / (1.0 - self.beta1 ** self.t)

        for p, m_arr, v_arr in zip(self.parameters, self.m, self.v):
            if p.grad is None:
                continue
            s = p.shape
            if len(s) == 1:
                for i in range(s[0]):
                    g = p.grad[i]
                    m_arr[i] = self.beta1 * m_arr[i] + (1.0 - self.beta1) * g
                    v_arr[i] = self.beta2 * v_arr[i] + (1.0 - self.beta2) * (g * g)
                    p.data[i] -= lr_t * m_arr[i] / (math.sqrt(v_arr[i]) + self.eps)
            elif len(s) == 2:
                for i in range(s[0]):
                    for j in range(s[1]):
                        g = p.grad[i][j]
                        m_arr[i][j] = self.beta1 * m_arr[i][j] + (1.0 - self.beta1) * g
                        v_arr[i][j] = self.beta2 * v_arr[i][j] + (1.0 - self.beta2) * (g * g)
                        p.data[i][j] -= lr_t * m_arr[i][j] / (math.sqrt(v_arr[i][j]) + self.eps)
