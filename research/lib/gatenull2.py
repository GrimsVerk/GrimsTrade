"""Pure functions for lane gate-null-2 (research/cards/gate-null-2.md): placebo families for a
dose-slope gate and a vectorised Newey-West slope t. No function here reads a file, a price or
the network; randomness comes only from the `numpy.random.Generator` passed in."""

from __future__ import annotations

import numpy as np

SHIFT_EARLIER: list[int] = list(range(25, 104, 2))  # F1: W33/W34/W36
SHIFT_BOTH: list[int] = [s * k for k in range(13, 90, 4) for s in (1, -1)]  # F1b: W29/W32
PRE, POST = 103, 89  # dose history needed before / after the sample for every shift


def nw_slope_t(y: np.ndarray, x: np.ndarray, lags: int) -> tuple[np.ndarray, np.ndarray]:
    """Slope b and Newey-West (Bartlett, `lags`) t of y on [1, x] for every column of x
    (shape T x K, or T). Equals the slope element of the full sandwich (inv X'X meat inv X'X)
    with scores summed per row, as in `wide11_events.ols_dk` with one asset."""
    x2 = x[:, None] if x.ndim == 1 else x
    xc = x2 - x2.mean(axis=0)
    yc = y - y.mean()
    sxx = (xc * xc).sum(axis=0)
    b = (xc * yc[:, None]).sum(axis=0) / sxx
    u = yc[:, None] - xc * b
    h = xc * u
    s = (h * h).sum(axis=0)
    for lag in range(1, lags + 1):
        s = s + 2 * (1 - lag / (lags + 1)) * (h[lag:] * h[:-lag]).sum(axis=0)
    t = b / np.sqrt(s / sxx**2)
    return b, t


def ar1(rng: np.random.Generator, n: int, phi: float, burn: int = 2000) -> np.ndarray:
    """Stationary Gaussian AR(1) with unit innovation variance (exact start)."""
    e = rng.standard_normal(n + burn)
    out = np.empty(n + burn)
    out[0] = e[0] / np.sqrt(1 - phi * phi) if phi < 1 else e[0]
    for i in range(1, n + burn):
        out[i] = phi * out[i - 1] + e[i]
    return out[burn:]


def garch_t(
    rng: np.random.Generator,
    n: int,
    ar: float = 0.05,
    alpha: float = 0.10,
    beta: float = 0.85,
    df: float = 5.0,
    burn: int = 500,
) -> np.ndarray:
    """r_t = ar r_{t-1} + s_t z_t, z Student-t(df) at unit variance, GARCH(1, 1) variance
    with unconditional variance 1."""
    m = n + burn
    z = rng.standard_t(df, m) / np.sqrt(df / (df - 2))
    omega = 1 - alpha - beta
    r = np.zeros(m)
    v = 1.0
    eps = 0.0
    for i in range(1, m):
        v = omega + alpha * eps * eps + beta * v
        eps = np.sqrt(v) * z[i]
        r[i] = ar * r[i - 1] + eps
    return r[burn:]


def shifted(dose_ext: np.ndarray, shifts: list[int], pre: int, n: int) -> np.ndarray:
    """T x K matrix of x_{t-k} for the sample t = 0..n-1, where dose_ext[pre + t] = x_t."""
    return np.column_stack([dose_ext[pre - k : pre - k + n] for k in shifts])


def phase_surrogates(rng: np.random.Generator, x: np.ndarray, m: int) -> np.ndarray:
    """m Fourier phase-randomised surrogates of x (shape n x m): same amplitude spectrum and
    mean, independent uniform phases (the zero and, for even n, the Nyquist term kept real)."""
    n = len(x)
    f = np.fft.rfft(x - x.mean())
    ph = rng.uniform(0, 2 * np.pi, (m, len(f)))
    ph[:, 0] = 0.0
    if n % 2 == 0:
        ph[:, -1] = 0.0
    s = np.fft.irfft(np.abs(f)[None, :] * np.exp(1j * ph), n=n, axis=1)
    out: np.ndarray = (s + x.mean()).T
    return out


def iaaft_surrogates(
    rng: np.random.Generator, x: np.ndarray, m: int, iters: int = 100
) -> np.ndarray:
    """m IAAFT surrogates of x (n x m): the same values as x in a new order whose amplitude
    spectrum matches x's (Schreiber and Schmitz 1996). Stops when no rank order changes or
    after `iters` rounds."""
    n = len(x)
    amp = np.abs(np.fft.rfft(x))
    srt = np.sort(x)
    s = np.stack([rng.permutation(x) for _ in range(m)])
    order = np.argsort(s, axis=1)
    for _ in range(iters):
        f = np.fft.rfft(s, axis=1)
        s = np.fft.irfft(amp[None, :] * np.exp(1j * np.angle(f)), n=n, axis=1)
        new = np.argsort(s, axis=1)
        s = np.empty_like(s)
        np.put_along_axis(s, new, np.broadcast_to(srt, s.shape), axis=1)
        if np.array_equal(new, order):
            break
        order = new
    out: np.ndarray = s.T
    return out


def block_bootstrap(rng: np.random.Generator, x: np.ndarray, m: int, block: int) -> np.ndarray:
    """m circular block-bootstrap copies of x (n x m), fixed block length."""
    n = len(x)
    nb = -(-n // block)
    starts = rng.integers(0, n, (m, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(m, -1)[:, :n] % n
    out: np.ndarray = x[idx].T
    return out


def rotations(rng: np.random.Generator, x: np.ndarray, m: int, gap: int) -> np.ndarray:
    """x rotated circularly by m distinct random offsets in [gap, n - gap] (n x m)."""
    n = len(x)
    offs = rng.choice(np.arange(gap, n - gap + 1), size=m, replace=False)
    out: np.ndarray = np.column_stack([np.roll(x, int(o)) for o in offs])
    return out


def rank_high(true: float | np.ndarray, placebo: np.ndarray) -> np.ndarray:
    """1 + number of placebo values strictly above `true` (placebo: ... x K, last axis)."""
    out: np.ndarray = 1 + (placebo > np.asarray(true)[..., None]).sum(axis=-1)
    return out


def n_eff(x: np.ndarray) -> float:
    """N / (1 + 2 sum of autocorrelations up to the first non-positive lag) (gate-power)."""
    xc = x - x.mean()
    n = len(xc)
    v = float(xc @ xc)
    tot = 0.0
    for lag in range(1, n // 2):
        r = float(xc[lag:] @ xc[:-lag]) / v
        if r <= 0:
            break
        tot += r
    return n / (1 + 2 * tot)


def acf1(x: np.ndarray) -> float:
    xc = x - x.mean()
    return float(xc[1:] @ xc[:-1]) / float(xc @ xc)
