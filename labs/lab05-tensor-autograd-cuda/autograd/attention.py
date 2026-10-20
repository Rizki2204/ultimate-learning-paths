import math
from autograd.tensor import Tensor
from autograd.ops import transpose, matmul_raw, mul_raw, softmax_raw, shape

def scaled_dot_product_attention(Q, K, V):
    """
    Computes Scaled Dot-Product Attention:
    Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V
    """
    d_k = Q.shape[1]
    scale = 1.0 / math.sqrt(d_k)

    # 1. Q * K^T
    K_T = Tensor(transpose(K.data), requires_grad=K.requires_grad)
    scores = Q.matmul(K_T)

    # 2. Scale
    scaled_scores = scores * scale

    # 3. Softmax along row axis
    probs_data = softmax_raw(scaled_scores.data)
    probs = Tensor(probs_data, requires_grad=True)

    # 4. Output = probs * V
    out = probs.matmul(V)

    # Set up custom reverse-mode gradient tape for attention
    if Q.requires_grad or K.requires_grad or V.requires_grad:
        out._parents = [Q, K, V]
        def _backward():
            # dL/dV = probs^T * dL/dOut
            if V.requires_grad:
                probs_T = transpose(probs_data)
                dV = matmul_raw(probs_T, out.grad)
                V.accumulate_grad(dV)

            # dL/dProbs = dL/dOut * V^T
            V_T = transpose(V.data)
            dProbs = matmul_raw(out.grad, V_T)

            # Softmax backward: dScores = probs * (dProbs - sum(dProbs * probs, axis=-1))
            # dScores_i = probs_i * (dProbs_i - dot(dProbs_row, probs_row))
            r, c = shape(probs_data)
            dScores = [[0.0] * c for _ in range(r)]
            for i in range(r):
                dot_prod = sum(dProbs[i][j] * probs_data[i][j] for j in range(c))
                for j in range(c):
                    dScores[i][j] = probs_data[i][j] * (dProbs[i][j] - dot_prod) * scale

            # dL/dQ = dScores * K
            if Q.requires_grad:
                dQ = matmul_raw(dScores, K.data)
                Q.accumulate_grad(dQ)

            # dL/dK = dScores^T * Q
            if K.requires_grad:
                dScores_T = transpose(dScores)
                dK = matmul_raw(dScores_T, Q.data)
                K.accumulate_grad(dK)

        out._creator = _backward

    return out

def simulated_cuda_matmul(A, B, tile_size=4):
    """
    Simulates a CUDA 2D Tiled Matrix Multiplication Kernel:
    Models thread blocks, shared memory loading, barrier synchronization (__syncthreads),
    and coalesced memory loads.
    """
    M, K = shape(A)
    K2, N = shape(B)
    assert K == K2, f"Shape mismatch: {M}x{K} vs {K2}x{N}"

    C = [[0.0] * N for _ in range(M)]
    num_tiles = (K + tile_size - 1) // tile_size

    # Simulate thread block grid
    for by in range((M + tile_size - 1) // tile_size):
        for bx in range((N + tile_size - 1) // tile_size):
            # Shared memory allocations for the tile
            tile_A = [[0.0] * tile_size for _ in range(tile_size)]
            tile_B = [[0.0] * tile_size for _ in range(tile_size)]

            # Accumulators per thread in the block
            acc = [[0.0] * tile_size for _ in range(tile_size)]

            for t in range(num_tiles):
                # 1. Collaborative loading of tiles from Global Memory into Shared Memory
                for ty in range(tile_size):
                    row = by * tile_size + ty
                    col = t * tile_size
                    for tx in range(tile_size):
                        if row < M and (col + tx) < K:
                            tile_A[ty][tx] = A[row][col + tx]
                        else:
                            tile_A[ty][tx] = 0.0

                for ty in range(tile_size):
                    row = t * tile_size + ty
                    col = bx * tile_size
                    for tx in range(tile_size):
                        if row < K and (col + tx) < N:
                            tile_B[ty][tx] = B[row][col + tx]
                        else:
                            tile_B[ty][tx] = 0.0

                # __syncthreads() barrier simulation: all threads finished loading

                # 2. Compute partial dot products from shared memory tiles
                for ty in range(tile_size):
                    for tx in range(tile_size):
                        for k in range(tile_size):
                            acc[ty][tx] += tile_A[ty][k] * tile_B[k][tx]

                # __syncthreads() barrier simulation before next tile load

            # 3. Store final computed results to global memory
            for ty in range(tile_size):
                row = by * tile_size + ty
                for tx in range(tile_size):
                    col = bx * tile_size + tx
                    if row < M and col < N:
                        C[row][col] = acc[ty][tx]

    return C
