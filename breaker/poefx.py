"""ctypes wrapper around poefx.c (exact integer evaluator of the PO alpha-EFX optimum)."""
import ctypes
import os
import subprocess
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "poefx.c")
LIB = os.path.join(HERE, "libpoefx.dylib")

if not os.path.exists(LIB) or os.path.getmtime(LIB) < os.path.getmtime(SRC):
    subprocess.check_call(["cc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB, SRC])
_lib = ctypes.CDLL(LIB)
_lib.eval_inst.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_longlong), ctypes.POINTER(ctypes.c_longlong)]
_lib.eval_inst.restype = ctypes.c_int


def _frac(num, den):
    if den == 0:
        return None  # +inf
    if den < 0:
        return None
    return Fraction(num, den)


def evaluate(V):
    """V: list of n rows of m positive ints. Returns dict with exact F* etc."""
    n, m = len(V), len(V[0])
    arr = (ctypes.c_longlong * (n * m))(*[int(x) for row in V for x in row])
    out = (ctypes.c_longlong * 9)()
    rc = _lib.eval_inst(n, m, arr, out)
    if rc != 0:
        raise RuntimeError(f"eval_inst rc={rc}")
    idx = out[3]
    own = []
    for _ in range(m):
        own.append(idx % n)
        idx //= n
    return {
        "Fstar": _frac(out[0], out[1]),
        "po_count": out[2],
        "argmax_owner": own,
        "best_any": _frac(out[4], out[5]),
        "frontier": out[6],
        "second": _frac(out[7], out[8]) if out[8] > 0 else None,
    }


def thm2(K):
    return [
        [3 * K, 2 * K + 2, K, K, 1, 1, K, 2, 1],
        [2 * K + 2, 3 * K, 1, K, K, 1, K, 1, 2],
        [3 * K, 2 * K + 2, 1, 1, K, K, K, 2, 1],
        [2 * K + 2, 3 * K, K, 1, 1, K, K, 1, 2],
    ]


if __name__ == "__main__":
    import time
    for K in [6, 7, 8, 10, 12, 20, 50, 100]:
        t = time.time()
        r = evaluate(thm2(K))
        print(K, r["Fstar"], float(r["Fstar"]), "bound", Fraction(2, 3) + Fraction(1, K), "po", r["po_count"], "front", r["frontier"], "any", r["best_any"], f"{time.time()-t:.2f}s", r["argmax_owner"])


SRC2 = os.path.join(HERE, "poefx_dfs.c")
LIB2 = os.path.join(HERE, "libpoefx_dfs.dylib")
if not os.path.exists(LIB2) or os.path.getmtime(LIB2) < os.path.getmtime(SRC2):
    subprocess.check_call(["cc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB2, SRC2])
_lib2 = ctypes.CDLL(LIB2)
_lib2.fstar_dfs.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_longlong), ctypes.c_longlong, ctypes.c_longlong,
                            ctypes.c_longlong, ctypes.c_longlong, ctypes.POINTER(ctypes.c_longlong), ctypes.POINTER(ctypes.c_int)]


def evaluate_dfs(V, theta=Fraction(1, 2), candlimit=5_000_000, nodelimit=50_000_000):
    """status 1: F* = returned value (>= theta); 0: F* < theta (all theta-EFX allocations dominated);
    -1: node limit hit (returned value is an unresolved candidate); -2: too many candidates."""
    n, m = len(V), len(V[0])
    arr = (ctypes.c_longlong * (n * m))(*[int(x) for row in V for x in row])
    out = (ctypes.c_longlong * 5)()
    own = (ctypes.c_int * m)()
    _lib2.fstar_dfs(n, m, arr, theta.numerator, theta.denominator, candlimit, nodelimit, out, own)
    st = out[0]
    F = None
    if st in (1, -1):
        F = Fraction(out[1], out[2]) if out[2] > 0 else None
    return {"status": st, "Fstar": F, "cands": out[3], "checks": out[4], "argmax_owner": list(own)}
