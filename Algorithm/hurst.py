#!/usr/bin/python

def hurst(price, min_lag=2, max_lag=100):
    import numpy as np
    lags = np.arange(min_lag, max_lag+1)
    tau = [np.std(np.subtract(price[lag:], price[:-lags])) for lag in lags]
    m = np.polyfit(np.log10(lags), np.log10(tau), 1)
    return m, lags, tau

    """
    N = 10000
    rand = np.cumsum(np.random.randn(N) + 0.01)
    mr = np.cumsum(np.sin(np.linspace(0, N/3*np.pi, N))/2 + 1)
    tr = np.cumsum(np.arange(N)/N)
    
    m_rand, lag_rand, rs_rand = hurst(rand)
    m_mr, lag_mr, rs_mr = hurst(mr)
    m_tr, lag_tr, rs_tr = hurst(rt)
    
    print(f"Hurst(Random):\t{m_rand[0]:.3f}")
    print(f"Hurst(MR):\t{m_mr[0]:.3f}")
    print(f"Hurst(TR):\t{m_tr[0]:.3f}")
    """
