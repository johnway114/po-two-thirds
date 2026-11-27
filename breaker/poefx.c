// Exact evaluator: optimal alpha-EFX value over Pareto-optimal complete allocations.
// For an instance v (n agents x m goods, positive integers), returns
//   F* = max over PO allocations A of alpha(A),
//   alpha(A) = min_{i != j, |A_j| >= 2} v_i(A_i) / (v_i(A_j) - min_{g in A_j} v_i(g))
// (alpha(A) = +inf, encoded den = 0, when no constraint applies).
// All arithmetic is integer; ratios compared by cross-multiplication.
#include <stdlib.h>
#include <string.h>

#define MAXN 6
#define MAXM 12

typedef struct {
    long long u[MAXN];
    long long num, den; // alpha = num/den, den==0 => +inf
    long long idx;
} rec_t;

static int g_n;

static int cmp_prof(const void *a, const void *b) {
    const rec_t *x = a, *y = b;
    for (int i = 0; i < g_n; i++) {
        if (x->u[i] != y->u[i]) return x->u[i] > y->u[i] ? -1 : 1;
    }
    return 0;
}

// a/b > c/d ? (den 0 means +inf)
static int gt(long long a, long long b, long long c, long long d) {
    if (b == 0) return d != 0;
    if (d == 0) return 0;
    return (__int128)a * d > (__int128)c * b;
}

static long long ipow(int n, int m) { long long r = 1; for (int k = 0; k < m; k++) r *= n; return r; }

// out[0], out[1]: F* num/den. out[2]: #PO allocations. out[3]: argmax alloc index (base-n digits, good 0 = least significant)
// out[4], out[5]: best alpha over ALL allocations (ignoring PO). out[6]: #distinct maximal profiles.
// out[7], out[8]: second best distinct alpha among PO allocations (num/den), den=-1 if none.
// Returns 0 on success.
int eval_inst(int n, int m, const long long *v, long long *out) {
    if (n > MAXN || m > MAXM || n < 1) return -1;
    g_n = n;
    long long N = ipow(n, m);
    rec_t *R = malloc(sizeof(rec_t) * N);
    if (!R) return -2;
    int own[MAXM];
    long long bestAllN = 0, bestAllD = 1;
    for (long long idx = 0; idx < N; idx++) {
        long long t = idx;
        for (int g = 0; g < m; g++) { own[g] = t % n; t /= n; }
        long long val[MAXN][MAXN]; long long mn[MAXN][MAXN]; int cnt[MAXN];
        memset(val, 0, sizeof val); memset(cnt, 0, sizeof cnt);
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) mn[i][j] = (long long)4e18;
        for (int g = 0; g < m; g++) {
            int j = own[g]; cnt[j]++;
            for (int i = 0; i < n; i++) {
                long long x = v[i * m + g];
                val[i][j] += x;
                if (x < mn[i][j]) mn[i][j] = x;
            }
        }
        long long an = 1, ad = 0;
        for (int j = 0; j < n; j++) {
            if (cnt[j] < 2) continue;
            for (int i = 0; i < n; i++) {
                if (i == j) continue;
                long long num = val[i][i], den = val[i][j] - mn[i][j];
                if (gt(an, ad, num, den)) { an = num; ad = den; }
            }
        }
        rec_t *r = &R[idx];
        for (int i = 0; i < n; i++) r->u[i] = val[i][i];
        r->num = an; r->den = ad; r->idx = idx;
        if (gt(an, ad, bestAllN, bestAllD)) { bestAllN = an; bestAllD = ad; }
    }
    qsort(R, N, sizeof(rec_t), cmp_prof);
    long long cap = 1024, F = 0;
    long long (*front)[MAXN] = malloc(sizeof(long long[MAXN]) * cap);
    long long bestN = -1, bestD = 1, bestIdx = -1, poCount = 0;
    long long secN = -1, secD = -1;
    int prevPO = 0;
    for (long long k = 0; k < N; k++) {
        int po;
        if (k > 0 && cmp_prof(&R[k], &R[k - 1]) == 0) {
            po = prevPO;
        } else {
            po = 1;
            for (long long f = 0; f < F; f++) {
                int dom = 1;
                for (int i = 0; i < n; i++) if (front[f][i] < R[k].u[i]) { dom = 0; break; }
                if (dom) {
                    po = 0;
                    if (f > 0) { // move-to-front heuristic (order of frontier is irrelevant for correctness)
                        long long tmp[MAXN];
                        long long h = f / 2;
                        memcpy(tmp, front[h], sizeof tmp); memcpy(front[h], front[f], sizeof tmp); memcpy(front[f], tmp, sizeof tmp);
                    }
                    break;
                }
            }
            if (po) {
                if (F == cap) { cap *= 2; front = realloc(front, sizeof(long long[MAXN]) * cap); }
                memcpy(front[F], R[k].u, sizeof(long long) * n); F++;
            }
        }
        prevPO = po;
        if (po) {
            poCount++;
            if (bestIdx < 0 || gt(R[k].num, R[k].den, bestN, bestD)) {
                if (bestIdx >= 0) { secN = bestN; secD = bestD; }
                bestN = R[k].num; bestD = R[k].den; bestIdx = R[k].idx;
            } else if (gt(bestN, bestD, R[k].num, R[k].den) && (secD < 0 || gt(R[k].num, R[k].den, secN, secD))) {
                secN = R[k].num; secD = R[k].den;
            }
        }
    }
    out[0] = bestN; out[1] = bestD; out[2] = poCount; out[3] = bestIdx;
    out[4] = bestAllN; out[5] = bestAllD; out[6] = F; out[7] = secN; out[8] = secD;
    free(front); free(R);
    return 0;
}
