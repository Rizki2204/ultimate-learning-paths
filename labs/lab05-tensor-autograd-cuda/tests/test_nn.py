import unittest
from autograd.tensor import Tensor
from autograd.nn import Linear, Sequential
from autograd.optim import SGD, Adam

class TestNeuralNetwork(unittest.TestCase):
    def test_linear_layer_forward_and_backward(self):
        fc = Linear(3, 2, bias=True)
        x = Tensor([[1.0, 2.0, 3.0]])
        out = fc(x)
        self.assertEqual(out.shape, (1, 2))

        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(fc.weight.grad)
        self.assertIsNotNone(fc.bias.grad)

    def test_optimizer_step(self):
        fc = Linear(2, 1, bias=False)
        init_w = [list(row) for row in fc.weight.data]

        x = Tensor([[1.0, 2.0]])
        y = Tensor([[5.0]])

        pred = fc(x)
        diff = pred - y
        loss = (diff * diff).sum()
        loss.backward()

        opt = SGD(fc.parameters(), lr=0.1)
        opt.step()

        # Weight should have changed in opposite direction of gradient
        self.assertNotEqual(fc.weight.data, init_w)

if __name__ == "__main__":
    unittest.main()
