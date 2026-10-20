import unittest
from autograd.tensor import Tensor
from autograd.attention import scaled_dot_product_attention, simulated_cuda_matmul
from autograd.ops import matmul_raw

class TestAttentionAndCUDA(unittest.TestCase):
    def test_scaled_dot_product_attention_forward(self):
        # Q: (2, 2), K: (2, 2), V: (2, 2)
        Q = Tensor([[1.0, 0.0],
                    [0.0, 1.0]], requires_grad=True)
        K = Tensor([[1.0, 0.0],
                    [0.0, 1.0]], requires_grad=True)
        V = Tensor([[10.0, 20.0],
                    [30.0, 40.0]], requires_grad=True)

        out = scaled_dot_product_attention(Q, K, V)
        self.assertEqual(out.shape, (2, 2))

        loss = out.sum()
        loss.backward()

        self.assertIsNotNone(Q.grad)
        self.assertIsNotNone(K.grad)
        self.assertIsNotNone(V.grad)

    def test_simulated_cuda_tiled_matmul(self):
        # 6x6 matrix multiplication with 4x4 tile size
        A = [[float(i * 6 + j) for j in range(6)] for i in range(6)]
        B = [[float(j * 6 + i + 1) for j in range(6)] for i in range(6)]

        golden = matmul_raw(A, B)
        cuda_sim = simulated_cuda_matmul(A, B, tile_size=4)

        for i in range(6):
            for j in range(6):
                self.assertAlmostEqual(cuda_sim[i][j], golden[i][j], places=5)

if __name__ == "__main__":
    unittest.main()
