import unittest
from autograd.tensor import Tensor
from autograd.ops import transpose, matmul_raw

class TestTensorOperations(unittest.TestCase):
    def test_tensor_creation_and_shapes(self):
        t1 = Tensor([1.0, 2.0, 3.0])
        self.assertEqual(t1.shape, (3,))

        t2 = Tensor([[1.0, 2.0], [3.0, 4.0]])
        self.assertEqual(t2.shape, (2, 2))

    def test_transpose_and_matmul(self):
        # A: (2, 3), B: (3, 2)
        A = [[1.0, 2.0, 3.0],
             [4.0, 5.0, 6.0]]
        B = [[7.0, 8.0],
             [9.0, 1.0],
             [2.0, 3.0]]
        # C[0][0] = 1*7 + 2*9 + 3*2 = 7 + 18 + 6 = 31
        # C[0][1] = 1*8 + 2*1 + 3*3 = 8 + 2 + 9 = 19
        # C[1][0] = 4*7 + 5*9 + 6*2 = 28 + 45 + 12 = 85
        # C[1][1] = 4*8 + 5*1 + 6*3 = 32 + 5 + 18 = 55
        C = matmul_raw(A, B)
        self.assertEqual(C, [[31.0, 19.0], [85.0, 55.0]])

        tA = Tensor(A)
        tB = Tensor(B)
        tC = tA.matmul(tB)
        self.assertEqual(tC.data, [[31.0, 19.0], [85.0, 55.0]])

if __name__ == "__main__":
    unittest.main()
