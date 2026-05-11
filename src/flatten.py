import numpy as np


def plane_subtract(data):
    """Fit and remove a least-squares plane from the height channel (index 0).

    Parameters
    ----------
    data : ndarray, shape (M, N, C)
        Multi-channel AFM array; height is channel 0, in metres.

    Returns
    -------
    ndarray, shape (M, N), float64
        Height channel with best-fit plane removed, in metres.
    """
    z = data[:, :, 0].astype(np.float64)
    m, n = z.shape

    yi, xi = np.mgrid[0:m, 0:n]
    ones = np.ones(m * n)
    A = np.column_stack([xi.ravel(), yi.ravel(), ones])

    coeffs, _, _, _ = np.linalg.lstsq(A, z.ravel(), rcond=None)
    plane = (A @ coeffs).reshape(m, n)

    return z - plane
