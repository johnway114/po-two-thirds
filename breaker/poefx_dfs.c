// Scalable exact evaluator for larger instances (n<=8, m<=24).
// fstar_dfs: enumerate all allocations with alpha(A) >= theta by pruned DFS, sort them by alpha
// descending, and test each for Pareto optimality with a pruned DFS for a dominating allocation.
// The first PO one gives F* (if F* >= theta).  If none is PO, F* < theta (certificate: every
// theta-EFX allocation has an explicit dominator, which the caller can re-verify).
// All arithmetic is integer; alpha comparisons by 128-bit cross-multiplication.
#include <stdlib.h>
#include <string.h>

#define MAXN 8
#define MAXM 24

static int N, M;
static long long V[MAXN][MAXM];
static int ord[MAXM];           // goods order for DFS
static long long suf[MAXN][MAXM + 1]; // suf[i][k] = sum of v_i over goods ord[k..]
static long long TN, TD;        // theta = TN/TD

typedef struct { signed char own[MAXM]; long long an, ad; } cand_t;
static cand_t *C; static long long nC, capC, limC;

static int own[MAXM];
static long long val[MAXN][MAXN], mnv[MAXN][MAXN]; static int cnt[MAXN];

static int ge_theta(long long num, long long den) { // num/den >= TN/TD, den>0
    return (__int128)num * TD >= (__int128)TN * den;
}

static int overflow;

static void dfs_efx(int k) {
    if (overflow) return;
    // prune: for i, j with cnt[j] >= 2: need v_i(A_i) final >= theta * (val[i][j]-mn[i][j]) (monotone in A_j).
    for (int j = 0; j < N; j++) {
        if (cnt[j] < 2) continue;
        for (int i = 0; i < N; i++) {
            if (i == j) continue;
            long long ub = val[i][i] + suf[i][k];
            if (!ge_theta(ub, val[i][j] - mnv[i][j])) return;
        }
    }
    if (k == M) {
        long long an = 1, ad = 0;
        for (int j = 0; j < N; j++) {
            if (cnt[j] < 2) continue;
            for (int i = 0; i < N; i++) {
                if (i == j) continue;
                long long num = val[i][i], den = val[i][j] - mnv[i][j];
                if (ad == 0 || (__int128)num * ad < (__int128)an * den) { an = num; ad = den; }
            }
        }
        if (nC == capC) {
            if (capC >= limC) { overflow = 1; return; }
            capC = capC ? capC * 2 : 4096; C = realloc(C, sizeof(cand_t) * capC);
        }
        for (int g = 0; g < M; g++) C[nC].own[g] = (signed char)own[g];
        C[nC].an = an; C[nC].ad = ad; nC++;
        return;
    }
    int g = ord[k];
    for (int j = 0; j < N; j++) {
        long long savedmn[MAXN];
        own[g] = j; cnt[j]++;
        for (int i = 0; i < N; i++) {
            savedmn[i] = mnv[i][j];
            val[i][j] += V[i][g];
            if (V[i][g] < mnv[i][j]) mnv[i][j] = V[i][g];
        }
        dfs_efx(k + 1);
        cnt[j]--;
        for (int i = 0; i < N; i++) { val[i][j] -= V[i][g]; mnv[i][j] = savedmn[i]; }
    }
}

// ---- dominance search ----
static long long need[MAXN];   // targets
static long long cur[MAXN];
static int down[MAXM];         // dominator assignment
static long long dnodes, dlimit;

static int dfs_dom(int k) {
    if (++dnodes > dlimit) return -1;
    int active = 0;
    for (int i = 0; i < N; i++) {
        long long d = need[i] - cur[i];
        if (d > 0) { active++; if (suf[i][k] < d) return 0; }
    }
    if (active == 0) {
        for (int kk = k; kk < M; kk++) down[ord[kk]] = 0; // any completion works (values positive)
        // give remaining goods to agent 0 (any choice keeps all targets met)
        return 1;
    }
    if (k == M) return 0;
    // relaxation: sum_g max_i v_i(g)/d_i over remaining goods must reach #active (scaled, in doubles as a heuristic prune only if clearly short)
    {
        double tot = 0;
        for (int kk = k; kk < M; kk++) {
            int g = ord[kk]; double best = 0;
            for (int i = 0; i < N; i++) {
                long long d = need[i] - cur[i];
                if (d > 0) { double r = (double)V[i][g] / (double)d; if (r > best) best = r; }
            }
            tot += best > 1 ? 1 : best;
        }
        if (tot < active - 1e-9 * active - 1e-12) return 0; // safe: exact bound is >= this up to fp; margin tiny
    }
    int g = ord[k];
    // try agents in order of largest unmet deficit-normalized value first
    int idx[MAXN]; double key[MAXN];
    for (int i = 0; i < N; i++) {
        long long d = need[i] - cur[i];
        idx[i] = i; key[i] = d > 0 ? (double)V[i][g] / d : -1.0 / (1 + V[i][g]);
    }
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) if (key[idx[b]] > key[idx[a]]) { int t = idx[a]; idx[a] = idx[b]; idx[b] = t; }
    for (int t = 0; t < N; t++) {
        int i = idx[t];
        down[g] = i; cur[i] += V[i][g];
        int r = dfs_dom(k + 1);
        cur[i] -= V[i][g];
        if (r != 0) return r;
    }
    return 0;
}

// returns 1 dominated (dom filled), 0 PO, -1 node limit
static int dominated(const signed char *a, int *dom) {
    long long u[MAXN] = {0};
    for (int g = 0; g < M; g++) u[a[g]] += V[(int)a[g]][g];
    for (int s = 0; s < N; s++) {
        for (int i = 0; i < N; i++) { need[i] = u[i] + (i == s); cur[i] = 0; }
        dnodes = 0;
        int r = dfs_dom(0);
        if (r == 1) {
            // fill unassigned (when early success) : recompute by rerun semantics -> assign rest to agent s
            for (int g = 0; g < M; g++) dom[g] = down[g];
            return 1;
        }
        if (r < 0) return -1;
    }
    return 0;
}

static int cmp_c(const void *x, const void *y) {
    const cand_t *a = x, *b = y;
    if (a->ad == 0 && b->ad == 0) return 0;
    if (a->ad == 0) return -1;
    if (b->ad == 0) return 1;
    __int128 l = (__int128)a->an * b->ad, r = (__int128)b->an * a->ad;
    return l > r ? -1 : (l < r ? 1 : 0);
}

// out: [0]=status (1 found PO with alpha>=theta, 0 none -> F*<theta, -1 node limit, -2 cand overflow)
// [1],[2] = F* num/den, [3] = #candidates, [4] = #dominance checks; own_out[m] = argmax allocation.
int fstar_dfs(int n, int m, const long long *v, long long tn, long long td, long long candlimit,
              long long nodelimit, long long *out, int *own_out) {
    N = n; M = m; TN = tn; TD = td; limC = candlimit; dlimit = nodelimit; overflow = 0;
    for (int i = 0; i < n; i++) for (int g = 0; g < m; g++) V[i][g] = v[i * m + g];
    // order goods by max value descending
    for (int g = 0; g < m; g++) ord[g] = g;
    for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) {
        long long ma = 0, mb = 0;
        for (int i = 0; i < n; i++) { if (V[i][ord[a]] > ma) ma = V[i][ord[a]]; if (V[i][ord[b]] > mb) mb = V[i][ord[b]]; }
        if (mb > ma) { int t = ord[a]; ord[a] = ord[b]; ord[b] = t; }
    }
    for (int i = 0; i < n; i++) { suf[i][m] = 0; for (int k = m - 1; k >= 0; k--) suf[i][k] = suf[i][k + 1] + V[i][ord[k]]; }
    memset(val, 0, sizeof val); memset(cnt, 0, sizeof cnt);
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) mnv[i][j] = (long long)4e18;
    nC = 0;
    dfs_efx(0);
    out[3] = nC;
    if (overflow) { out[0] = -2; return 0; }
    qsort(C, nC, sizeof(cand_t), cmp_c);
    long long checks = 0;
    int dom[MAXM];
    out[0] = 0;
    for (long long c = 0; c < nC; c++) {
        // skip candidates with identical profile to an earlier dominated one is not needed for correctness
        checks++;
        int r = dominated(C[c].own, dom);
        if (r == 0) {
            out[0] = 1; out[1] = C[c].an; out[2] = C[c].ad;
            for (int g = 0; g < m; g++) own_out[g] = C[c].own[g];
            break;
        }
        if (r < 0) { out[0] = -1; out[1] = C[c].an; out[2] = C[c].ad; for (int g = 0; g < m; g++) own_out[g] = C[c].own[g]; break; }
    }
    out[4] = checks;
    return 0;
}
