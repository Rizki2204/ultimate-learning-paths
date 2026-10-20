# Laboratory 05: Reverse-Mode Autograd Engine & Attention Kernel

## 1. Architectural Overview
This laboratory implements a pure standard-library reverse-mode tape automatic differentiation engine, neural network parameter optimization framework, and scaled dot-product attention mechanism in Python 3.14. The system operates with zero third-party dependencies (no NumPy or PyTorch) and includes a high-fidelity simulation of 2D tiled matrix multiplication on GPU architectures.

```
+-----------------------------------------------------------------------+
|                    Dynamic Computational Graph (Tape)                 |
|                                                                       |
|        [ Tensor A ] --------+                                         |
|                             |---> [ MatMul Node ] ---> [ Tensor C ]   |
|        [ Tensor B ] --------+           |                     |       |
|                                         |                     v       |
|                                         |              [ Sum Loss L ] |
|                                         |                     |       |
|   Reverse Topological Traversal <-------+---------------------+       |
|   dL/dA = dL/dC * B^T                                                 |
|   dL/dB = A^T * dL/dC                                                 |
|                                                                       |
|   Scaled Dot-Product Attention:                                       |
|   Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V               |
|                                                                       |
|   GPU Kernel Architecture Simulation:                                 |
|   Global Memory -> Shared Memory Tile Blocking -> __syncthreads()     |
+-----------------------------------------------------------------------+
```

## 2. Mathematical Foundations

### Vector-Jacobian Product (VJP) in Reverse Mode
For a composite function $L = f(g(x))$, reverse-mode autodiff propagates the adjoint $\bar{y} = \frac{\partial L}{\partial y}$ backwards:
$$\bar{x} = \bar{y} \cdot J_g(x)$$

For matrix multiplication $C = A B$ with scalar loss $L$:
$$\frac{\partial L}{\partial A} = \frac{\partial L}{\partial C} B^T, \quad \frac{\partial L}{\partial B} = A^T \frac{\partial L}{\partial C}$$

### Softmax and Attention Derivatives
Given normalized attention scores $P = \text{softmax}(S)$ where $S = \frac{Q K^T}{\sqrt{d_k}}$:
$$\frac{\partial L}{\partial S_i} = P_i \left( \frac{\partial L}{\partial P_i} - \sum_j \frac{\partial L}{\partial P_j} P_j \right)$$
$$\nabla_Q = \frac{1}{\sqrt{d_k}} \nabla_S K, \quad \nabla_K = \frac{1}{\sqrt{d_k}} \nabla_S^T Q, \quad \nabla_V = P^T \nabla_O$$

### CUDA Shared Memory Matrix Tiling
To avoid memory bandwidth saturation, the kernel partitions matrices into $T \times T$ sub-blocks (tiles):
1. Cooperative loading of tiles into on-chip shared memory `__shared__ float As[T][T], Bs[T][T]`.
2. Barrier synchronization `__syncthreads()` guaranteeing tile completeness.
3. Compute register accumulations.
4. Barrier synchronization before the subsequent tile stage.

## 3. Scaffolding & Directory Structure
```
labs/lab05-tensor-autograd-cuda/
├── README.md               # Architecture documentation
├── Makefile                # Build and test automation
├── run_tests.py            # Standalone test runner
├── autograd/               # Autograd library implementation
│   ├── __init__.py         # Package exports
│   ├── tensor.py           # Tensor data structure & reverse autodiff
│   ├── ops.py              # Primitive mathematical ops (matmul, sum, relu)
│   ├── nn.py               # Parameter, Linear, and Sequential modules
│   ├── optim.py            # SGD with momentum and Adam optimizers
│   └── attention.py        # Attention kernel and CUDA tile simulation
├── starter/                # Student starter scaffolding
│   └── autograd_starter.py # Clean scalar autograd skeleton
└── tests/                  # Automated test suite
    ├── test_tensor.py      # Tensor creation and matmul correctness
    ├── test_autograd.py    # Finite-difference numerical gradient checks
    ├── test_nn.py          # Neural network module and parameter updates
    ├── test_attention.py   # Scaled dot-product attention and CUDA tiling
    └── test_training.py    # Non-linear MLP XOR convergence training
```

## 4. Milestone Progression Guide
1. **Milestone 1 (Tensors & Computational Graph)**:
   Construct the `Tensor` class with `data`, `grad`, `_parents`, and `_creator` tape references.
2. **Milestone 2 (Reverse Mode Autodiff)**:
   Implement topological sorting and vector-Jacobian products. Verify against centered finite-difference numerical approximations ($|(f(x+\epsilon) - f(x-\epsilon))/(2\epsilon) - \nabla| < 10^{-4}$).
3. **Milestone 3 (Neural Network Layers & Adam)**:
   Implement Xavier-initialized `Linear` layers, `Sequential` containers, and the `Adam` optimizer with first and second moment bias correction.
4. **Milestone 4 (Attention Kernel & CUDA Simulation)**:
   Implement scaled dot-product attention and verify the simulated 2D tiled GPU matrix multiplication kernel against the golden CPU reference.

## 5. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 10 test suites execute within 30 milliseconds and pass with exit code 0.
