import math

def shape(data):
    if not isinstance(data, list):
        return ()
    if not data or not isinstance(data[0], list):
        return (len(data),)
    return (len(data), len(data[0]))

def zeros(s):
    if not s:
        return 0.0
    if len(s) == 1:
        return [0.0] * s[0]
    return [[0.0] * s[1] for _ in range(s[0])]

def copy_data(data):
    if not isinstance(data, list):
        return data
    if not data or not isinstance(data[0], list):
        return list(data)
    return [list(row) for row in data]

def transpose(data):
    s = shape(data)
    if len(s) < 2:
        return copy_data(data)
    r, c = s
    return [[data[i][j] for i in range(r)] for j in range(c)]

def matmul_raw(A, B):
    sA = shape(A)
    sB = shape(B)
    rA, cA = sA
    rB, cB = sB
    if cA != rB:
        raise ValueError(f"Incompatible shapes for matmul: {sA} and {sB}")
    out = [[0.0] * cB for _ in range(rA)]
    for i in range(rA):
        for k in range(cA):
            a_ik = A[i][k]
            for j in range(cB):
                out[i][j] += a_ik * B[k][j]
    return out

def add_raw(A, B):
    sA = shape(A)
    sB = shape(B)
    if sA == sB:
        if len(sA) == 0:
            return A + B
        if len(sA) == 1:
            return [A[i] + B[i] for i in range(sA[0])]
        return [[A[i][j] + B[i][j] for j in range(sA[1])] for i in range(sA[0])]
    # Broadcast B (1D row bias) into A (2D)
    if len(sA) == 2 and len(sB) == 1 and sA[1] == sB[0]:
        return [[A[i][j] + B[j] for j in range(sA[1])] for i in range(sA[0])]
    raise ValueError(f"Cannot broadcast shapes {sA} and {sB}")

def sub_raw(A, B):
    sA = shape(A)
    sB = shape(B)
    if sA == sB:
        if len(sA) == 0:
            return A - B
        if len(sA) == 1:
            return [A[i] - B[i] for i in range(sA[0])]
        return [[A[i][j] - B[i][j] for j in range(sA[1])] for i in range(sA[0])]
    raise ValueError(f"Cannot subtract shapes {sA} and {sB}")

def mul_raw(A, B):
    sA = shape(A)
    sB = shape(B)
    if sA == sB:
        if len(sA) == 0:
            return A * B
        if len(sA) == 1:
            return [A[i] * B[i] for i in range(sA[0])]
        return [[A[i][j] * B[i][j] for j in range(sA[1])] for i in range(sA[0])]
    # Scalar multiplication
    if len(sB) == 0:
        if len(sA) == 1:
            return [A[i] * B for i in range(sA[0])]
        return [[A[i][j] * B for j in range(sA[1])] for i in range(sA[0])]
    raise ValueError(f"Cannot multiply shapes {sA} and {sB}")

def sum_raw(A):
    s = shape(A)
    if len(s) == 0:
        return A
    if len(s) == 1:
        return sum(A)
    return sum(sum(row) for row in A)

def relu_raw(A):
    s = shape(A)
    if len(s) == 1:
        return [x if x > 0 else 0.0 for x in A]
    return [[x if x > 0 else 0.0 for x in row] for row in A]

def sigmoid_raw(A):
    def sig(x):
        return 1.0 / (1.0 + math.exp(-max(min(x, 50.0), -50.0)))
    s = shape(A)
    if len(s) == 1:
        return [sig(x) for x in A]
    return [[sig(x) for x in row] for row in A]

def softmax_raw(A):
    s = shape(A)
    if len(s) == 1:
        max_val = max(A)
        exps = [math.exp(x - max_val) for x in A]
        total = sum(exps)
        return [x / total for x in exps]
    out = []
    for row in A:
        max_val = max(row)
        exps = [math.exp(x - max_val) for x in row]
        total = sum(exps)
        out.append([x / total for x in exps])
    return out
