import unittest
from autograd.tensor import Tensor

class TestAutograd(unittest.TestCase):
    def test_scalar_chain_rule(self):
        # f(x, y) = x * y + x * x
        # df/dx = y + 2x; df/dy = x
        x = Tensor(3.0, requires_grad=True)
        y = Tensor(4.0, requires_grad=True)
        z = x * y + x * x
        z.backward()
        # df/dx = 4 + 2*3 = 10
        # df/dy = 3
        self.assertAlmostEqual(x.grad, 10.0, places=5)
        self.assertAlmostEqual(y.grad, 3.0, places=5)

    def test_numerical_gradient_check(self):
        eps = 1e-5

        def compute_loss(val):
            x = Tensor(val, requires_grad=True)
            y = Tensor(2.5, requires_grad=False)
            out = (x * x * y + x * 3.0).sum()
            return out.data

        x_val = 1.75
        x = Tensor(x_val, requires_grad=True)
        y = Tensor(2.5, requires_grad=False)
        out = (x * x * y + x * 3.0).sum()
        out.backward()
        analytical_grad = x.grad

        f_plus = compute_loss(x_val + eps)
        f_minus = compute_loss(x_val - eps)
        numerical_grad = (f_plus - f_minus) / (2.0 * eps)

        self.assertAlmostEqual(analytical_grad, numerical_grad, delta=1e-4)

    def test_matmul_gradient(self):
        # A: (2, 2), B: (2, 2)
        # C = A * B; L = sum(C)
        # dL/dA = [[1, 1], [1, 1]] * B^T = sum of rows of B
        A = Tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
        B = Tensor([[5.0, 6.0], [7.0, 8.0]], requires_grad=True)
        C = A.matmul(B)
        loss = C.sum()
        loss.backward()

        # B^T is [[5, 7], [6, 8]]
        # dL/dA should be [[5+6, 7+8], [5+6, 7+8]] = [[11, 15], [11, 15]]
        self.assertEqual(A.grad, [[11.0, 15.0], [11.0, 15.0]])

if __name__ == "__main__":
    unittest.main()
