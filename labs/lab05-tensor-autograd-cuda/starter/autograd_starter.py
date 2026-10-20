"""
Starter Scaffolding: Reverse-Mode Automatic Differentiation

Exercise Instructions:
Implement Tensor wrapping, backward computation graph chaining,
and scalar addition/multiplication gradients.
"""

class StarterTensor:
    def __init__(self, data, requires_grad=False):
        self.data = float(data)
        self.requires_grad = requires_grad
        self.grad = 0.0
        self._creator = None
        self._parents = []

    def __repr__(self):
        return f"StarterTensor(data={self.data}, grad={self.grad})"

    def __add__(self, other):
        other = other if isinstance(other, StarterTensor) else StarterTensor(other)
        out = StarterTensor(self.data + other.data, requires_grad=self.requires_grad or other.requires_grad)

        if out.requires_grad:
            out._parents = [self, other]
            def _backward():
                if self.requires_grad:
                    self.grad += out.grad
                if other.requires_grad:
                    other.grad += out.grad
            out._creator = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, StarterTensor) else StarterTensor(other)
        out = StarterTensor(self.data * other.data, requires_grad=self.requires_grad or other.requires_grad)

        if out.requires_grad:
            out._parents = [self, other]
            def _backward():
                if self.requires_grad:
                    self.grad += out.grad * other.data
                if other.requires_grad:
                    other.grad += out.grad * self.data
            out._creator = _backward

        return out

    def backward(self, gradient=1.0):
        self.grad = gradient
        topo = []
        visited = set()

        def build_topo(node):
            if id(node) not in visited:
                visited.add(id(node))
                for p in node._parents:
                    build_topo(p)
                topo.append(node)

        build_topo(self)
        for node in reversed(topo):
            if node._creator is not None:
                node._creator()

if __name__ == "__main__":
    x = StarterTensor(3.0, requires_grad=True)
    y = StarterTensor(4.0, requires_grad=True)
    z = x * y + x  # z = 3*4 + 3 = 15; dz/dx = 4 + 1 = 5; dz/dy = 3
    z.backward()
    print(f"z={z.data}, dz/dx={x.grad}, dz/dy={y.grad}")
