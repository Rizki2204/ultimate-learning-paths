from autograd.ops import (
    shape, zeros, copy_data, transpose, matmul_raw, add_raw, sub_raw,
    mul_raw, sum_raw, relu_raw, sigmoid_raw
)

class Tensor:
    def __init__(self, data, requires_grad=False):
        self.data = copy_data(data)
        self.shape = shape(self.data)
        self.requires_grad = requires_grad
        self.grad = None
        self._creator = None
        self._parents = []

    def zero_grad(self):
        self.grad = None

    def __repr__(self):
        return f"Tensor({self.data}, requires_grad={self.requires_grad})"

    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(add_raw(self.data, other.data), requires_grad=self.requires_grad or other.requires_grad)

        if out.requires_grad:
            out._parents = [self, other]
            def _backward():
                if self.requires_grad:
                    # If broadcasting happened (e.g. self is 2D and other is 1D bias)
                    g = out.grad
                    if len(self.shape) == 1 and len(shape(g)) == 2:
                        # sum across columns
                        g = [sum(row[j] for row in g) for j in range(self.shape[0])]
                    self.accumulate_grad(g)
                if other.requires_grad:
                    g = out.grad
                    if len(other.shape) == 1 and len(shape(g)) == 2:
                        # sum across rows
                        g = [sum(g[i][j] for i in range(len(g))) for j in range(other.shape[0])]
                    other.accumulate_grad(g)
            out._creator = _backward

        return out

    def __sub__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(sub_raw(self.data, other.data), requires_grad=self.requires_grad or other.requires_grad)

        if out.requires_grad:
            out._parents = [self, other]
            def _backward():
                if self.requires_grad:
                    self.accumulate_grad(out.grad)
                if other.requires_grad:
                    neg_g = mul_raw(out.grad, -1.0)
                    other.accumulate_grad(neg_g)
            out._creator = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(mul_raw(self.data, other.data), requires_grad=self.requires_grad or other.requires_grad)

        if out.requires_grad:
            out._parents = [self, other]
            def _backward():
                if self.requires_grad:
                    g = mul_raw(out.grad, other.data)
                    self.accumulate_grad(g)
                if other.requires_grad:
                    g = mul_raw(out.grad, self.data)
                    other.accumulate_grad(g)
            out._creator = _backward

        return out

    def matmul(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(matmul_raw(self.data, other.data), requires_grad=self.requires_grad or other.requires_grad)

        if out.requires_grad:
            out._parents = [self, other]
            def _backward():
                # dL/dA = dL/dOut * B^T
                # dL/dB = A^T * dL/dOut
                if self.requires_grad:
                    B_T = transpose(other.data)
                    dA = matmul_raw(out.grad, B_T)
                    self.accumulate_grad(dA)
                if other.requires_grad:
                    A_T = transpose(self.data)
                    dB = matmul_raw(A_T, out.grad)
                    other.accumulate_grad(dB)
            out._creator = _backward

        return out

    def relu(self):
        out = Tensor(relu_raw(self.data), requires_grad=self.requires_grad)

        if out.requires_grad:
            out._parents = [self]
            def _backward():
                if self.requires_grad:
                    s = self.shape
                    if len(s) == 1:
                        mask = [1.0 if x > 0 else 0.0 for x in self.data]
                    else:
                        mask = [[1.0 if x > 0 else 0.0 for x in row] for row in self.data]
                    g = mul_raw(out.grad, mask)
                    self.accumulate_grad(g)
            out._creator = _backward

        return out

    def sigmoid(self):
        sig_data = sigmoid_raw(self.data)
        out = Tensor(sig_data, requires_grad=self.requires_grad)

        if out.requires_grad:
            out._parents = [self]
            def _backward():
                if self.requires_grad:
                    # dSigmoid = sig * (1 - sig) * out.grad
                    s = self.shape
                    if len(s) == 1:
                        dsig = [s_val * (1.0 - s_val) for s_val in sig_data]
                    else:
                        dsig = [[s_val * (1.0 - s_val) for s_val in row] for row in sig_data]
                    g = mul_raw(out.grad, dsig)
                    self.accumulate_grad(g)
            out._creator = _backward

        return out

    def sum(self):
        val = sum_raw(self.data)
        out = Tensor(val, requires_grad=self.requires_grad)

        if out.requires_grad:
            out._parents = [self]
            def _backward():
                if self.requires_grad:
                    s = self.shape
                    if len(s) == 0:
                        g = out.grad
                    elif len(s) == 1:
                        g = [out.grad] * s[0]
                    else:
                        g = [[out.grad] * s[1] for _ in range(s[0])]
                    self.accumulate_grad(g)
            out._creator = _backward

        return out

    def accumulate_grad(self, g):
        if self.grad is None:
            self.grad = copy_data(g)
        else:
            self.grad = add_raw(self.grad, g)

    def backward(self, gradient=None):
        if gradient is None:
            if self.shape == ():
                gradient = 1.0
            elif len(self.shape) == 1:
                gradient = [1.0] * self.shape[0]
            else:
                gradient = [[1.0] * self.shape[1] for _ in range(self.shape[0])]

        self.grad = gradient

        # Build topological sort
        topo = []
        visited = set()

        def build_topo(node):
            if id(node) not in visited:
                visited.add(id(node))
                for parent in node._parents:
                    build_topo(parent)
                topo.append(node)

        build_topo(self)

        # Backpropagation in reverse topological order
        for node in reversed(topo):
            if node._creator is not None:
                node._creator()
