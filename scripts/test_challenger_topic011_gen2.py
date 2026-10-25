#!/usr/bin/env python3
"""
scripts/test_challenger_topic011_gen2.py

Adversarial Stress Test & Empirical Verification Harness for Topic 011 Rebuild.
Author: Challenger 1 (Gen 2) - Empirical Algorithmic Challenger
Repository: ultimate-learning-paths

Covers:
1. Bab 08 PCA ZeroDivision Challenge (IndustrialPCA)
2. Bab 09 Tensor Mode Product & Tucker HOSVD Challenge (tensor_mode_product)
3. Cholesky vs LU Numerical Stability & FLOP Count Challenge
"""

import os
import sys
import math
import time
import textwrap
from typing import List, Tuple, Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CURRICULUM_DIR = os.path.join(BASE_DIR, "curriculum", "01-fondasi-matematika", "011-aljabar-linier-teori-matriks")

class TestResult:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.passed = False
        self.message = ""
        self.details: Dict[str, Any] = {}
        self.duration = 0.0

    def pass_test(self, message: str, **kwargs):
        self.passed = True
        self.message = message
        self.details = kwargs
        return self

    def fail_test(self, message: str, **kwargs):
        self.passed = False
        self.message = message
        self.details = kwargs
        return self


# =============================================================================
# CODE EXTRACTORS (DIRECT FROM CURRICULUM MARKDOWN TO GUARANTEE INTEGRITY)
# =============================================================================

def get_industrial_pca_class():
    """Extract and compile IndustrialPCA directly from Bab 08 markdown."""
    bab08_path = os.path.join(CURRICULUM_DIR, "08-pca-analisis-komponen-utama.md")
    with open(bab08_path, "r", encoding="utf-8") as f:
        text = f.read()
    pos = text.find("class IndustrialPCA:")
    if pos == -1:
        raise ValueError(f"Could not find class IndustrialPCA in {bab08_path}")
    end = text.find("def run_test_suite", pos)
    code = text[pos:end]
    namespace = {"math": math, "List": List, "Tuple": Tuple}
    exec(code, namespace)
    return namespace["IndustrialPCA"]


def get_bab09_functions():
    """Extract tensor functions from Bab 09 markdown."""
    bab09_path = os.path.join(CURRICULUM_DIR, "09-aljabar-multilinier-dekomposisi-tensor.md")
    with open(bab09_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    pos_pure = text.find("def pure_tensor_unfold_3d")
    end_pure = text.find("def run_pure_python_tensor_demo", pos_pure)
    code_pure = text[pos_pure:end_pure]
    ns_pure = {"math": math, "List": List, "Tuple": Tuple}
    exec(code_pure, ns_pure)

    ns_numpy = {}
    try:
        import numpy as np
        pos_np = text.find("def tensor_unfold(")
        line_start = text.rfind("\n", 0, pos_np) + 1
        end_np = text.find("# --- PENGUJIAN 1", pos_np)
        code_np = textwrap.dedent(text[line_start:end_np])
        ns_numpy = {"np": np, "List": List, "Tuple": Tuple, "math": math}
        exec(code_np, ns_numpy)
    except Exception as e:
        ns_numpy["error"] = str(e)

    return ns_pure, ns_numpy


def get_bab06_cholesky():
    """Extract pure python Cholesky from Bab 06 markdown."""
    bab06_path = os.path.join(CURRICULUM_DIR, "06-matriks-simetris-definit-positif.md")
    with open(bab06_path, "r", encoding="utf-8") as f:
        text = f.read()
    pos = text.find("def pure_cholesky(")
    end = text.find("if __name__", pos)
    code = text[pos:end]
    namespace = {"math": math, "list": list, "tuple": tuple}
    exec(code, namespace)
    return namespace["pure_cholesky"], namespace["pure_cholesky_solve"]


def get_bab01_lu():
    """Extract pure python LU with partial pivot from Bab 01 markdown."""
    bab01_path = os.path.join(CURRICULUM_DIR, "01-vektor-eliminasi-matriks.md")
    with open(bab01_path, "r", encoding="utf-8") as f:
        text = f.read()
    pos = text.find("def lu_factorization_partial_pivot(")
    end = text.find("if __name__", pos)
    code = text[pos:end]
    namespace = {"math": math, "List": List, "Tuple": Tuple}
    exec(code, namespace)
    return namespace["lu_factorization_partial_pivot"], namespace["forward_solve"], namespace["back_solve"], namespace["mat_vec_mul"]


# =============================================================================
# CHALLENGE 1: BAB 08 PCA ZERO-DIVISION & ADVERSARIAL STRESS SUITE
# =============================================================================

def run_pca_stress_suite() -> List[TestResult]:
    results = []
    IndustrialPCA = get_industrial_pca_class()

    # 1. Pure Diagonal Covariance: Var(X1) = 5.0 > Var(X2) = 2.0
    tr = TestResult("PCA Pure Diagonal (Var1 > Var2)", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [
            [-math.sqrt(5.0), 0.0],
            [math.sqrt(5.0), 0.0],
            [0.0, -math.sqrt(2.0)],
            [0.0, math.sqrt(2.0)]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        ev = pca.explained_variance_
        
        # Check alignment: w1 along x-axis [1, 0]
        assert abs(abs(c0[0]) - 1.0) < 1e-10 and abs(c0[1]) < 1e-10, f"w1 not aligned with X1: {c0}"
        assert abs(abs(c1[1]) - 1.0) < 1e-10 and abs(c1[0]) < 1e-10, f"w2 not aligned with X2: {c1}"
        assert abs(dot) < 1e-10, f"Eigenvectors not orthogonal: dot={dot}"
        
        tr.pass_test(f"Orthogonal eigenvectors dot={dot:.2e}, zero ZeroDivisionError, w1 aligned with X1", w1=c0, w2=c1, ev=ev)
    except Exception as e:
        tr.fail_test(f"Exception raised: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 2. Pure Diagonal Covariance: Var(X1) = 2.0 < Var(X2) = 5.0
    tr = TestResult("PCA Pure Diagonal (Var1 < Var2)", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [
            [-math.sqrt(2.0), 0.0],
            [math.sqrt(2.0), 0.0],
            [0.0, -math.sqrt(5.0)],
            [0.0, math.sqrt(5.0)]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        
        # Check alignment: w1 along y-axis [0, 1]
        assert abs(abs(c0[1]) - 1.0) < 1e-10 and abs(c0[0]) < 1e-10, f"w1 not aligned with X2: {c0}"
        assert abs(abs(c1[0]) - 1.0) < 1e-10 and abs(c1[1]) < 1e-10, f"w2 not aligned with X1: {c1}"
        assert abs(dot) < 1e-10, f"Eigenvectors not orthogonal: dot={dot}"
        
        tr.pass_test(f"Orthogonal eigenvectors dot={dot:.2e}, w1 correctly selected on X2", w1=c0, w2=c1)
    except Exception as e:
        tr.fail_test(f"Exception raised: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 3. Degenerate Isotropic Covariance [[3.0, 0.0], [0.0, 3.0]]
    tr = TestResult("PCA Degenerate Isotropic Matrix", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [
            [-math.sqrt(3.0), 0.0],
            [math.sqrt(3.0), 0.0],
            [0.0, -math.sqrt(3.0)],
            [0.0, math.sqrt(3.0)]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        ev = pca.explained_variance_
        
        assert abs(dot) < 1e-10, f"Eigenvectors not orthogonal in isotropic case: dot={dot}"
        assert abs(ev[0] - ev[1]) < 1e-10, f"Eigenvalues should be equal: {ev}"
        
        tr.pass_test(f"Isotropic case handled cleanly, equal eigenvalues {ev[0]:.4f}, dot={dot:.2e}", w1=c0, w2=c1, ev=ev)
    except Exception as e:
        tr.fail_test(f"Exception raised: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 4. Perfectly Anti-Correlated Data (Collinear x2 = -2.5 x1)
    tr = TestResult("PCA Perfectly Anti-Correlated Data", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [
            [1.0, -2.5],
            [2.0, -5.0],
            [3.0, -7.5],
            [4.0, -10.0],
            [5.0, -12.5]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        ev = pca.explained_variance_
        
        assert abs(dot) < 1e-10, f"Non-orthogonal: {dot}"
        assert ev[1] < 1e-10, f"Second eigenvalue must be 0 for collinear data, got {ev[1]}"
        assert abs(pca.explained_variance_ratio_[0] - 1.0) < 1e-10, f"PC1 PVE should be 1.0, got {pca.explained_variance_ratio_[0]}"
        
        # Test 1D reconstruction
        pca1 = IndustrialPCA(n_components=1).fit(X)
        Z = pca1.transform(X)
        X_rec = pca1.inverse_transform(Z)
        rec_err = sum((X[i][j] - X_rec[i][j])**2 for i in range(len(X)) for j in range(2))
        assert rec_err < 1e-10, f"Collinear 1D reconstruction error must be 0, got {rec_err}"
        
        tr.pass_test(f"Collinear data has lambda2=0, PVE=100%, rec_err={rec_err:.2e}, dot={dot:.2e}", w1=c0, w2=c1, ev=ev)
    except Exception as e:
        tr.fail_test(f"Exception raised: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 5. Single-Point Data (n = 1) Boundary Defense
    tr = TestResult("PCA Single-Point Data Guard (n=1)", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [[42.0, 99.0]]
        pca = IndustrialPCA(n_components=1).fit(X)
        tr.fail_test("Allowed n=1 data without exception!")
    except ValueError as ve:
        tr.pass_test(f"Clean ValueError intercepted defensive guard: '{ve}'")
    except ZeroDivisionError as zde:
        tr.fail_test(f"Uncaught ZeroDivisionError on n=1: {zde}")
    except Exception as e:
        tr.fail_test(f"Unexpected exception type: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 6. Large Dynamic Range High (10^8 to 10^10)
    tr = TestResult("PCA High Dynamic Range (10^10)", "Bab 08 PCA")
    t0 = time.time()
    try:
        scale = 1e10
        X = [
            [1.0 * scale, 2.0 * scale],
            [2.0 * scale, 5.0 * scale],
            [3.0 * scale, 3.0 * scale],
            [5.0 * scale, 8.0 * scale],
            [9.0 * scale, 7.0 * scale]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        
        assert abs(dot) < 1e-8, f"Loss of orthogonality on large numbers: dot={dot}"
        assert abs(abs(c0[0]) - 0.8) < 1e-4 and abs(abs(c0[1]) - 0.6) < 1e-4, f"Direction distorted: {c0}"
        
        tr.pass_test(f"Orthogonality preserved (dot={dot:.2e}) on scale 10^10, direction consistent", w1=c0, w2=c1)
    except Exception as e:
        tr.fail_test(f"Exception raised on scale 10^10: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 7. Disparate Dynamic Range (X1 ~ 10^10, X2 ~ 10^-10)
    tr = TestResult("PCA Disparate Dynamic Range (10^10 vs 10^-10)", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [
            [-1e10, -1e-10],
            [1e10, 1e-10],
            [-2e10, -2e-10],
            [2e10, 2e-10]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        
        assert abs(dot) < 1e-8, f"Loss of orthogonality: dot={dot}"
        assert abs(c0[0]) > 0.999999, f"PC1 failed to capture dominant axis: {c0}"
        
        tr.pass_test(f"Disparate scales handled cleanly, dot={dot:.2e}, PC1 aligns with dominant axis", w1=c0, w2=c1)
    except Exception as e:
        tr.fail_test(f"Exception on disparate scales: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 8. Micro-Scale Dynamic Range (10^-10) - Investigation of Absolute Epsilon Guard
    tr = TestResult("PCA Micro-Scale (10^-10) Epsilon Threshold Probe", "Bab 08 PCA")
    t0 = time.time()
    try:
        scale = 1e-10
        # Strongly correlated data on micro scale: x2 = 2 * x1
        X = [
            [-1.0 * scale, -2.0 * scale],
            [1.0 * scale, 2.0 * scale],
            [-2.0 * scale, -4.0 * scale],
            [2.0 * scale, 4.0 * scale]
        ]
        pca = IndustrialPCA(n_components=2).fit(X)
        dot = pca.components_[0][0] * pca.components_[1][0] + pca.components_[0][1] * pca.components_[1][1]
        c0 = pca.components_[0]
        c1 = pca.components_[1]
        
        is_falsely_diagonal = (c0 == [1.0, 0.0] or c0 == [0.0, 1.0])
        if is_falsely_diagonal:
            tr.fail_test("CRITICAL NUMERICAL DEFECT: Fixed threshold `abs(S[0][1]) <= 1e-12` causes micro-scale correlated data (10^-10) to be falsely classified as diagonal!",
                         c0=c0, c1=c1, dot=dot)
        else:
            tr.pass_test(f"Correctly computed non-diagonal eigenvectors on micro scale: c0={c0}", c0=c0, dot=dot)
    except Exception as e:
        tr.fail_test(f"Exception on micro-scale: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 9. Constant Data (Zero Total Variance) - Division by Zero in PVE Probe
    tr = TestResult("PCA Constant Data (Zero Variance) DivZero Probe", "Bab 08 PCA")
    t0 = time.time()
    try:
        X = [
            [5.0, 5.0],
            [5.0, 5.0],
            [5.0, 5.0]
        ]
        pca = IndustrialPCA(n_components=1).fit(X)
        tr.pass_test("Constant data handled without exception", ev=pca.explained_variance_)
    except ZeroDivisionError as zde:
        tr.fail_test(f"VULNERABILITY CONFIRMED: Constant data triggers ZeroDivisionError in explained_variance_ratio_: {zde}")
    except ValueError as ve:
        tr.pass_test(f"Constant data cleanly rejected via ValueError: {ve}")
    except Exception as e:
        tr.fail_test(f"Unexpected exception on constant data: {type(e).__name__}: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    return results


# =============================================================================
# CHALLENGE 2: BAB 09 TENSOR MODE PRODUCT & HOSVD ADVERSARIAL SUITE
# =============================================================================

def run_tensor_adversarial_suite() -> List[TestResult]:
    results = []
    ns_pure, ns_numpy = get_bab09_functions()
    
    # 1. Pure Python 3D Mode-Product Axis Verification
    tr = TestResult("Bab 09 Pure Python 3D Mode-Product All Modes", "Bab 09 Tensor")
    t0 = time.time()
    try:
        pure_mode_prod = ns_pure["pure_tensor_mode_product_3d"]
        pure_unfold = ns_pure["pure_tensor_unfold_3d"]
        
        # Test tensor 2 x 3 x 4
        X = [[[float(i * 12 + j * 4 + k) for k in range(4)] for j in range(3)] for i in range(2)]
        
        # Mode 0 with matrix 5 x 2
        U0 = [[float(m + i) for i in range(2)] for m in range(5)]
        Y0 = pure_mode_prod(X, U0, mode=0)
        assert len(Y0) == 5 and len(Y0[0]) == 3 and len(Y0[0][0]) == 4, f"Shape mismatch Y0: ({len(Y0)}, {len(Y0[0])}, {len(Y0[0][0])})"
        
        # Mode 1 with matrix 6 x 3
        U1 = [[float(m + j) for j in range(3)] for m in range(6)]
        Y1 = pure_mode_prod(X, U1, mode=1)
        assert len(Y1) == 2 and len(Y1[0]) == 6 and len(Y1[0][0]) == 4, f"Shape mismatch Y1: ({len(Y1)}, {len(Y1[0])}, {len(Y1[0][0])})"
        
        # Mode 2 with matrix 7 x 4
        U2 = [[float(m + k) for k in range(4)] for m in range(7)]
        Y2 = pure_mode_prod(X, U2, mode=2)
        assert len(Y2) == 2 and len(Y2[0]) == 3 and len(Y2[0][0]) == 7, f"Shape mismatch Y2: ({len(Y2)}, {len(Y2[0])}, {len(Y2[0][0])})"
        
        tr.pass_test("Pure Python 3D mode product outputs exact shapes across all modes (0, 1, 2)")
    except Exception as e:
        tr.fail_test(f"Pure Python mode product failed: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # If NumPy is available, run deep multi-dimensional tensor contractions & HOSVD
    if "tensor_mode_product" in ns_numpy:
        import numpy as np
        tensor_mode_product = ns_numpy["tensor_mode_product"]
        tensor_unfold = ns_numpy["tensor_unfold"]
        hosvd_decomposition = ns_numpy["hosvd_decomposition"]

        # 2. NumPy Asymmetric 3D Tensor (2, 3, 4) Across Modes 0, 1, 2
        tr = TestResult("Tensor Mode Product (2, 3, 4) vs Einsum Oracle", "Bab 09 Tensor")
        t0 = time.time()
        try:
            np.random.seed(42)
            X = np.random.randn(2, 3, 4)
            
            # Mode 0
            M0 = np.random.randn(7, 2)
            Y0 = tensor_mode_product(X, M0, mode=0)
            Y0_oracle = np.einsum('ia,ajk->ijk', M0, X)
            assert Y0.shape == (7, 3, 4), f"Shape failed mode 0: {Y0.shape}"
            assert np.allclose(Y0, Y0_oracle, atol=1e-14), "Numerical values failed mode 0 vs einsum"
            
            # Mode 1
            M1 = np.random.randn(5, 3)
            Y1 = tensor_mode_product(X, M1, mode=1)
            Y1_oracle = np.einsum('ja,iak->ijk', M1, X)
            assert Y1.shape == (2, 5, 4), f"Shape failed mode 1: {Y1.shape}"
            assert np.allclose(Y1, Y1_oracle, atol=1e-14), "Numerical values failed mode 1 vs einsum"
            
            # Mode 2
            M2 = np.random.randn(9, 4)
            Y2 = tensor_mode_product(X, M2, mode=2)
            Y2_oracle = np.einsum('ka,ija->ijk', M2, X)
            assert Y2.shape == (2, 3, 9), f"Shape failed mode 2: {Y2.shape}"
            assert np.allclose(Y2, Y2_oracle, atol=1e-14), "Numerical values failed mode 2 vs einsum"
            
            tr.pass_test("All 3 modes on (2, 3, 4) matched einsum oracle to machine precision (<1e-14)")
        except Exception as e:
            tr.fail_test(f"Contraction failed: {e}")
        tr.duration = time.time() - t0
        results.append(tr)

        # 3. NumPy Asymmetric 3D Tensor (5, 2, 7) Across Modes 0, 1, 2
        tr = TestResult("Tensor Mode Product (5, 2, 7) vs Einsum Oracle", "Bab 09 Tensor")
        t0 = time.time()
        try:
            X = np.random.randn(5, 2, 7)
            M0 = np.random.randn(4, 5)
            M1 = np.random.randn(8, 2)
            M2 = np.random.randn(3, 7)
            
            Y0 = tensor_mode_product(X, M0, mode=0)
            Y1 = tensor_mode_product(X, M1, mode=1)
            Y2 = tensor_mode_product(X, M2, mode=2)
            
            assert Y0.shape == (4, 2, 7) and np.allclose(Y0, np.einsum('ia,ajk->ijk', M0, X), atol=1e-14)
            assert Y1.shape == (5, 8, 7) and np.allclose(Y1, np.einsum('ja,iak->ijk', M1, X), atol=1e-14)
            assert Y2.shape == (5, 2, 3) and np.allclose(Y2, np.einsum('ka,ija->ijk', M2, X), atol=1e-14)
            
            tr.pass_test("All 3 modes on (5, 2, 7) matched einsum oracle to machine precision")
        except Exception as e:
            tr.fail_test(f"Contraction failed: {e}")
        tr.duration = time.time() - t0
        results.append(tr)

        # 4. NumPy 4D Tensor (2, 3, 4, 5) Across Modes 0, 1, 2, 3
        tr = TestResult("Tensor Mode Product 4D (2, 3, 4, 5) vs Einsum Oracle", "Bab 09 Tensor")
        t0 = time.time()
        try:
            X = np.random.randn(2, 3, 4, 5)
            M0 = np.random.randn(6, 2)
            M1 = np.random.randn(7, 3)
            M2 = np.random.randn(8, 4)
            M3 = np.random.randn(9, 5)
            
            Y0 = tensor_mode_product(X, M0, mode=0)
            Y1 = tensor_mode_product(X, M1, mode=1)
            Y2 = tensor_mode_product(X, M2, mode=2)
            Y3 = tensor_mode_product(X, M3, mode=3)
            
            assert Y0.shape == (6, 3, 4, 5) and np.allclose(Y0, np.einsum('ia,ajkl->ijkl', M0, X), atol=1e-14)
            assert Y1.shape == (2, 7, 4, 5) and np.allclose(Y1, np.einsum('ja,iakl->ijkl', M1, X), atol=1e-14)
            assert Y2.shape == (2, 3, 8, 5) and np.allclose(Y2, np.einsum('ka,ijal->ijkl', M2, X), atol=1e-14)
            assert Y3.shape == (2, 3, 4, 9) and np.allclose(Y3, np.einsum('la,ijka->ijkl', M3, X), atol=1e-14)
            
            tr.pass_test("4D tensor contractions across all 4 modes verified against einsum oracle")
        except Exception as e:
            tr.fail_test(f"4D mode contraction failed: {e}")
        tr.duration = time.time() - t0
        results.append(tr)

        # 5. Tucker HOSVD Full-Rank Reconstruction Error on Asymmetric Tensors
        tr = TestResult("Tucker HOSVD Full-Rank Reconstruction Error", "Bab 09 Tensor")
        t0 = time.time()
        try:
            # Test 1: (2, 3, 4) full ranks [2, 3, 4]
            X1 = np.random.randn(2, 3, 4)
            core1, factors1 = hosvd_decomposition(X1, ranks=[2, 3, 4])
            recon1 = core1.copy()
            for m in range(3):
                recon1 = tensor_mode_product(recon1, factors1[m], mode=m)
            err1 = np.linalg.norm(X1 - recon1)
            
            # Test 2: (5, 2, 7) full ranks [5, 2, 7]
            X2 = np.random.randn(5, 2, 7)
            core2, factors2 = hosvd_decomposition(X2, ranks=[5, 2, 7])
            recon2 = core2.copy()
            for m in range(3):
                recon2 = tensor_mode_product(recon2, factors2[m], mode=m)
            err2 = np.linalg.norm(X2 - recon2)
            
            # Test 3: 4D (2, 3, 4, 5) full ranks [2, 3, 4, 5]
            X3 = np.random.randn(2, 3, 4, 5)
            core3, factors3 = hosvd_decomposition(X3, ranks=[2, 3, 4, 5])
            recon3 = core3.copy()
            for m in range(4):
                recon3 = tensor_mode_product(recon3, factors3[m], mode=m)
            err3 = np.linalg.norm(X3 - recon3)
            
            assert err1 < 1e-13, f"Full rank recon error (2, 3, 4) too high: {err1}"
            assert err2 < 1e-13, f"Full rank recon error (5, 2, 7) too high: {err2}"
            assert err3 < 1e-13, f"Full rank recon error 4D (2, 3, 4, 5) too high: {err3}"
            
            tr.pass_test(f"Full-rank HOSVD reconstruction error < 1e-13 across all 3D/4D tensors (err1={err1:.2e}, err2={err2:.2e}, err3={err3:.2e})")
        except Exception as e:
            tr.fail_test(f"HOSVD reconstruction failed: {e}")
        tr.duration = time.time() - t0
        results.append(tr)

        # 6. Tucker HOSVD Truncated Reconstruction & Error Bound
        tr = TestResult("Tucker HOSVD Truncated Error Bound", "Bab 09 Tensor")
        t0 = time.time()
        try:
            X = np.random.randn(2, 3, 4)
            ranks = [1, 2, 3]
            core, factors = hosvd_decomposition(X, ranks=ranks)
            
            assert core.shape == tuple(ranks), f"Core shape {core.shape} != {ranks}"
            recon = core.copy()
            for m in range(3):
                recon = tensor_mode_product(recon, factors[m], mode=m)
            err = np.linalg.norm(X - recon)
            
            # Theoretical upper bound: sqrt(sum_{m} sum_{j > Rm} sigma_m_j^2)
            sum_tail_sq = 0.0
            for m in range(3):
                X_m = tensor_unfold(X, mode=m)
                _, s_m, _ = np.linalg.svd(X_m, full_matrices=False)
                sum_tail_sq += np.sum(s_m[ranks[m]:] ** 2)
            bound = math.sqrt(sum_tail_sq)
            
            assert err <= bound + 1e-10, f"HOSVD error {err} violated theoretical bound {bound}!"
            tr.pass_test(f"Truncated HOSVD error {err:.4f} strictly bounded by De Lathauwer bound {bound:.4f}")
        except Exception as e:
            tr.fail_test(f"Truncated HOSVD failed: {e}")
        tr.duration = time.time() - t0
        results.append(tr)
    else:
        tr = TestResult("NumPy HOSVD Suite", "Bab 09 Tensor")
        tr.fail_test(f"NumPy not available in environment: {ns_numpy.get('error', 'unknown')}")
        results.append(tr)

    return results


# =============================================================================
# CHALLENGE 3: CHOLESKY VS LU NUMERICAL STABILITY & FLOP COUNT HARNESS
# =============================================================================

class FlopCounter:
    """Wrapper that counts arithmetic operations precisely."""
    def __init__(self):
        self.mult_div = 0
        self.add_sub = 0
        self.sqrts = 0

    def add(self): self.add_sub += 1
    def sub(self): self.add_sub += 1
    def mul(self): self.mult_div += 1
    def div(self): self.mult_div += 1
    def sqrt(self): self.sqrts += 1

    @property
    def total(self):
        return self.mult_div + self.add_sub + self.sqrts


def instrumented_cholesky(A: List[List[float]], fc: FlopCounter) -> List[List[float]]:
    """Instrumented version of Bab 06 Cholesky counting exact FLOPs."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = 0.0
            for k in range(j):
                s += L[i][k] * L[j][k]
                fc.mul()
                fc.add()
            if i == j:
                val = A[i][i] - s
                fc.sub()
                if val <= 1e-14:
                    raise ValueError(f"Not positive definite at {i}")
                L[i][j] = math.sqrt(val)
                fc.sqrt()
            else:
                diff = A[i][j] - s
                fc.sub()
                L[i][j] = diff / L[j][j]
                fc.div()
    return L


def instrumented_lu_no_pivot(A: List[List[float]], fc: FlopCounter) -> Tuple[List[List[float]], List[List[float]]]:
    """Instrumented version of standard LU factorization without pivoting."""
    n = len(A)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[A[i][j] for j in range(n)] for i in range(n)]
    for k in range(n - 1):
        for i in range(k + 1, n):
            m = U[i][k] / U[k][k]
            fc.div()
            L[i][k] = m
            for j in range(k, n):
                U[i][j] -= m * U[k][j]
                fc.mul()
                fc.sub()
    return L, U


def run_cholesky_lu_stability_suite() -> List[TestResult]:
    results = []
    
    # 1. FLOP Count Mathematical Rigor Validation
    tr = TestResult("Cholesky vs LU FLOP Count Asymptotic & Convergence", "Cholesky vs LU")
    t0 = time.time()
    try:
        sizes = [8, 16, 32, 64]
        records = []
        for n in sizes:
            # Generate diagonally dominant SPD matrix of size n
            A = [[0.0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    A[i][j] = float(i + 1) * float(j + 1) / n
                A[i][i] += float(n * 2)

            # Count Cholesky FLOPs
            fc_chol = FlopCounter()
            instrumented_cholesky(A, fc_chol)
            
            # Count LU FLOPs
            fc_lu = FlopCounter()
            instrumented_lu_no_pivot(A, fc_lu)
            
            ratio = fc_chol.total / fc_lu.total
            
            records.append({
                "n": n,
                "chol_total": fc_chol.total,
                "lu_total": fc_lu.total,
                "ratio": ratio,
                "theo_ratio": 0.5
            })
            
        # Verify asymptotic convergence:
        # At n=8, ratio <= 0.66; at n=64, ratio <= 0.52 (within 4% of 0.5 limit)
        assert records[0]["ratio"] <= 0.66, f"Ratio too high at n=8: {records[0]['ratio']}"
        assert records[-1]["ratio"] <= 0.52, f"Ratio failed to converge to 0.5 at n=64: {records[-1]['ratio']}"
        assert records[-1]["ratio"] < records[0]["ratio"], "Ratio did not decrease monotonically towards 0.5"
            
        tr.pass_test(f"Cholesky FLOPs confirmed converging to 50% of LU: ratio drops from {records[0]['ratio']:.4f} (n=8) to {records[-1]['ratio']:.4f} (n=64)", records=records)
    except Exception as e:
        tr.fail_test(f"FLOP count verification failed: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    # 2. Numerical Stability Across Condition Number Spectrum kappa in [10^1, 10^8]
    tr = TestResult("Numerical Stability Across kappa in [10^1, 10^8]", "Cholesky vs LU")
    t0 = time.time()
    try:
        import numpy as np
        import scipy.linalg
        
        condition_numbers = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8]
        stability_records = []
        n = 8
        
        for kappa in condition_numbers:
            # Generate random orthogonal Q via QR
            np.random.seed(int(kappa) % 1000 + 42)
            X = np.random.randn(n, n)
            Q, _ = np.linalg.qr(X)
            
            # Logarithmically spaced eigenvalues from 1.0 to kappa
            eigenvalues = np.logspace(0, math.log10(kappa), n)
            A = Q @ np.diag(eigenvalues) @ Q.T
            A = 0.5 * (A + A.T) # enforce exact symmetry
            
            # True solution x_true = [1.0, 1.0, ..., 1.0]
            x_true = np.ones(n, dtype=np.float64)
            b = A @ x_true
            
            # Solve via Cholesky
            L_chol = np.linalg.cholesky(A)
            y_chol = scipy.linalg.solve_triangular(L_chol, b, lower=True)
            x_chol = scipy.linalg.solve_triangular(L_chol.T, y_chol, lower=False)
            
            # Solve via LU with partial pivoting
            P, L_lu, U_lu = scipy.linalg.lu(A)
            y_lu = scipy.linalg.solve_triangular(L_lu, P.T @ b, lower=True)
            x_lu = scipy.linalg.solve_triangular(U_lu, y_lu, lower=False)
            
            # Relative forward error ||x - x_true|| / ||x_true||
            fwd_err_chol = np.linalg.norm(x_chol - x_true) / np.linalg.norm(x_true)
            fwd_err_lu = np.linalg.norm(x_lu - x_true) / np.linalg.norm(x_true)
            
            # Relative backward residual ||A x - b|| / (||A|| ||x|| + ||b||)
            res_chol = np.linalg.norm(A @ x_chol - b) / (np.linalg.norm(A) * np.linalg.norm(x_chol) + np.linalg.norm(b))
            res_lu = np.linalg.norm(A @ x_lu - b) / (np.linalg.norm(A) * np.linalg.norm(x_lu) + np.linalg.norm(b))
            
            stability_records.append({
                "kappa": kappa,
                "fwd_chol": float(fwd_err_chol),
                "fwd_lu": float(fwd_err_lu),
                "res_chol": float(res_chol),
                "res_lu": float(res_lu)
            })
            
            # Backward stability check: residual must be < 1e-13
            assert res_chol < 1e-13, f"Cholesky backward stability violated for kappa={kappa}: res={res_chol}"
            assert res_lu < 1e-13, f"LU backward stability violated for kappa={kappa}: res={res_lu}"
            
            # Forward error bound: fwd_err <= C * kappa * eps_mach
            eps_mach = np.finfo(np.float64).eps
            assert fwd_err_chol <= 100 * kappa * eps_mach, f"Cholesky forward error exceeded theoretical bound for kappa={kappa}"
            assert fwd_err_lu <= 100 * kappa * eps_mach, f"LU forward error exceeded theoretical bound for kappa={kappa}"
            
        tr.pass_test(f"Both Cholesky and LU backward stable (residual < 1e-13) and forward error bounded by kappa*eps up to kappa=10^8",
                     records=stability_records)
    except Exception as e:
        tr.fail_test(f"Condition number stability test failed: {e}")
    tr.duration = time.time() - t0
    results.append(tr)

    return results


# =============================================================================
# MAIN RUNNER
# =============================================================================

def main():
    print("=" * 80)
    print("  CHALLENGER 1 (GEN 2): EMPIRICAL ADVERSARIAL STRESS TEST HARNESS")
    print("  Topic 011: Computational Linear Algebra & Numerical Optimization")
    print("=" * 80)
    
    suite1 = run_pca_stress_suite()
    suite2 = run_tensor_adversarial_suite()
    suite3 = run_cholesky_lu_stability_suite()
    
    all_results = suite1 + suite2 + suite3
    
    passed_count = sum(1 for r in all_results if r.passed)
    failed_count = sum(1 for r in all_results if not r.passed)
    
    print("\n" + "-" * 80)
    print("DETAILED RESULTS:")
    print("-" * 80)
    
    for r in all_results:
        status_tag = "[PASS]" if r.passed else "[FAIL]"
        print(f"{status_tag} [{r.category}] {r.name} ({r.duration:.4f}s)")
        print(f"       Outcome: {r.message}")
        if r.details:
            for k, v in r.details.items():
                print(f"       * {k}: {v}")
                
    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(all_results)} tests executed | {passed_count} PASSED | {failed_count} FAILED")
    print("=" * 80)
    
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
