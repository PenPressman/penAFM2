import numpy as np


def compute_roughness(arr):
    """Compute surface roughness parameters from a flattened 2D height array.

    Parameters
    ----------
    arr : ndarray, shape (M, N)
        Height data in metres.

    Returns
    -------
    dict with keys:
        Ra  – arithmetic mean roughness (m)
        Rq  – RMS roughness (m)
        Rz  – peak-to-valley height (m)
    """
    z = arr.ravel().astype(np.float64)
    mean = z.mean()
    deviations = z - mean
    return {
        "Ra": float(np.mean(np.abs(deviations))),
        "Rq": float(np.sqrt(np.mean(deviations ** 2))),
        "Rz": float(z.max() - z.min()),
    }
