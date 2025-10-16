
import argparse
import json
import numpy as np
import pandas as pd
from pathlib import Path
import yaml

def project_simplex(v):
    n = v.shape[0]
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, n+1) > (cssv - 1))[0][-1]
    theta = (cssv[rho] - 1) / (rho + 1.0)
    w = np.maximum(v - theta, 0)
    return w

def softmax(x, axis=0):
    x = x - np.max(x, axis=axis, keepdims=True)
    ex = np.exp(x)
    return ex / (np.sum(ex, axis=axis, keepdims=True) + 1e-12)

def kl_div(Q, P):
    eps = 1e-12
    Q = np.clip(Q, eps, 1.0)
    P = np.clip(P, eps, 1.0)
    return np.sum(Q * (np.log(Q) - np.log(P)))

def build_sigma_matrix(df_norm: pd.DataFrame, sigma_ids):
    mats = []
    obs_index = None
    for sid in sigma_ids:
        sub = df_norm[df_norm["id"] == sid][["region","year","norm"]].copy()
        sub = sub.rename(columns={"norm": sid})
        if obs_index is None:
            obs_index = sub[["region","year"]]
            mats.append(sub[[sid]])
        else:
            merged = obs_index.merge(sub, on=["region","year"], how="left")
            mats.append(merged[[sid]])
    M = pd.concat(mats, axis=1).to_numpy(dtype=float)
    mask = ~np.isnan(M).any(axis=1)
    M = M[mask]
    return M, obs_index[mask].reset_index(drop=True)

def build_target_Q(M):
    avg = np.mean(M, axis=1, keepdims=True)
    Q = softmax(avg, axis=0)
    return Q.squeeze()

def loss_and_grad(w, M, Q):
    sigma_hat = M @ w
    P = softmax(sigma_hat.reshape(-1,1), axis=0).squeeze()
    L = kl_div(Q, P)
    grad = np.zeros_like(w)
    delta = 1e-3
    for i in range(len(w)):
        w_pos = project_simplex(w + np.eye(1, len(w), i).ravel()*delta)
        w_neg = project_simplex(w - np.eye(1, len(w), i).ravel()*delta)
        P_pos = softmax((M @ w_pos).reshape(-1,1), axis=0).squeeze()
        P_neg = softmax((M @ w_neg).reshape(-1,1), axis=0).squeeze()
        L_pos = kl_div(Q, P_pos)
        L_neg = kl_div(Q, P_neg)
        grad[i] = (L_pos - L_neg) / (np.linalg.norm(w_pos - w_neg) + 1e-12)
    return L, grad

def fit_weights(M, Q, max_iter=500, lr=0.1, tol=1e-6, seed=42):
    rng = np.random.default_rng(seed)
    K = M.shape[1]
    w = rng.random(K)
    w = project_simplex(w)
    prev = 1e18
    for t in range(max_iter):
        L, g = loss_and_grad(w, M, Q)
        if abs(prev - L) < tol:
            break
        prev = L
        w = w - lr * g
        w = project_simplex(w)
        if (t+1) % 50 == 0:
            lr = lr * 0.5
    return w, prev

def bootstrap_ci(M, Q, B=100, **fit_kwargs):
    N = M.shape[0]
    W = []
    Ls = []
    rng = np.random.default_rng(0)
    for b in range(B):
        idx = rng.integers(0, N, size=N)
        Mb = M[idx, :]
        Qb = Q[idx]
        Qb = Qb / (Qb.sum() + 1e-12)
        w, loss = fit_weights(Mb, Qb, **fit_kwargs)
        W.append(w)
        Ls.append(loss)
    W = np.stack(W, axis=0)
    mean = W.mean(axis=0)
    lo = np.percentile(W, 2.5, axis=0)
    hi = np.percentile(W, 97.5, axis=0)
    return mean, lo, hi, float(np.mean(Ls))

def main(config_path: str, df_norm_path: str = 'data/interim/indicators_normalized.csv', out_json='data/processed/weights_sigma.json'):
    cfg = yaml.safe_load(Path(config_path).read_text())
    sigma_ids = [i['id'] for i in cfg['latents']['sigma']['indicators']]
    df_norm = pd.read_csv(df_norm_path)
    M, obs = build_sigma_matrix(df_norm, sigma_ids)
    if M.size == 0:
        raise SystemExit('No matching rows for sigma indicators; ensure IDs align with normalized data.')
    Q = build_target_Q(M)
    w, loss = fit_weights(M, Q, max_iter=300, lr=0.2)
    mean, lo, hi, boot_loss = bootstrap_ci(M, Q, B=50, max_iter=200, lr=0.2)

    out = {
        'sigma_ids': sigma_ids,
        'weights_point': list(map(float, w)),
        'weights_bootstrap_mean': list(map(float, mean)),
        'weights_ci95_lo': list(map(float, lo)),
        'weights_ci95_hi': list(map(float, hi)),
        'loss': float(loss),
        'boot_loss_mean': float(boot_loss)
    }
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(out_json).write_text(json.dumps(out, indent=2), encoding='utf-8')
    print('Wrote', out_json, '=>', out)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--norm', default='data/interim/indicators_normalized.csv')
    ap.add_argument('--out', default='data/processed/weights_sigma.json')
    args = ap.parse_args()
    main(args.config, args.norm, args.out)
