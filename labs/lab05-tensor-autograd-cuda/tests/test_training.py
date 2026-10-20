import unittest
import random
from autograd.tensor import Tensor
from autograd.nn import Linear
from autograd.optim import Adam

class TestMLPTraining(unittest.TestCase):
    def test_xor_convergence(self):
        random.seed(42)

        # 2-layer network: 2 -> 4 -> 1
        fc1 = Linear(2, 4, bias=True)
        fc2 = Linear(4, 1, bias=True)

        params = fc1.parameters() + fc2.parameters()
        opt = Adam(params, lr=0.08)

        # XOR dataset
        X = Tensor([[0.0, 0.0],
                    [0.0, 1.0],
                    [1.0, 0.0],
                    [1.0, 1.0]])
        Y = Tensor([[0.0],
                    [1.0],
                    [1.0],
                    [0.0]])

        initial_loss = None
        final_loss = None

        for epoch in range(120):
            opt.zero_grad()

            h = fc1(X).sigmoid()
            out = fc2(h).sigmoid()

            diff = out - Y
            loss = (diff * diff).sum()

            if initial_loss is None:
                initial_loss = loss.data

            loss.backward()
            opt.step()

            final_loss = loss.data

        # Loss must have converged significantly
        self.assertLess(final_loss, initial_loss * 0.5)

if __name__ == "__main__":
    unittest.main()
