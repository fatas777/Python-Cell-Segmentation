"""
Some functions with the same/similar functionality to Matlab's bwmorph
Credit for spur, endpoints, and the baseline for most of this code to
 https://gist.github.com/bmabey/4dd36d9938b83742a88b6f68ac1901a6
 Added branchpoint function
"""
import numpy as np
import scipy.ndimage as ndi
from skimage import measure

LUT_DEL_MASK = np.array([[8, 4, 2], [16, 0, 1], [32, 64, 128]], dtype=np.uint8)

LUT_MASK = np.array([[8, 4, 2], [16, 256, 1], [32, 64, 128]], dtype=np.uint16)

"""
To make a LUT with 3x3 filter: lut = np.array([Function(n) for n in range(512)])
"""


def branchpoint_fcn(n):
    nhood = hood(n)
    if nhood[1, 1] == 1:
        count = np.sum(nhood) - 1
        if count > 2:
            return 1
        else:
            return 0
    else:
        return 0


def count_fcn(n):
    nhood = hood(n)
    if nhood[1, 1] == 1:
        (L, count) = measure.label(~nhood, return_num=True, connectivity=1)
        return count
    else:
        return 0


def branchpoints(image):
    init_LUT = np.array([branchpoint_fcn(n) for n in range(512)])
    im = np.array(image).astype(np.uint16)
    N = ndi.correlate(im, LUT_MASK, mode="constant")
    C = np.take(init_LUT, N)
    cnt_LUT = np.array([count_fcn(n) for n in range(512)])
    B = np.take(cnt_LUT, N)
    E = B == 1
    FC = ~E * C
    Vp = (B == 2) & ~E
    Vq = (B > 2) & ~E
    D = np.take(dil_LUT, Vq)
    M = (FC & Vp) & D
    bw = FC & ~M
    return bw


def endpoint_fcn(n):
    nhood = hood(n)
    if nhood[1, 1] == 1:
        (L, count) = measure.label(~nhood, return_num=True, connectivity=1)
        if count == 1:
            return 1
        else:
            return 0
    else:
        return 0


def endpoints(image):
    shape = image.shape
    if not np.all(np.in1d(image.flat, (0, 1))):
        raise ValueError("Image contains values other than 0 and 1")
    im = np.array(image).astype(np.uint16)
    im = np.pad(im, (1, 1), "constant", constant_values=0)
    N = ndi.correlate(im, LUT_MASK, mode="constant")
    D = np.take(EP_LUT, N)
    return D[1 : shape[0] + 1, 1 : shape[1] + 1]


def _bwmorph_luts(image, luts, n_iter=None, padding=0):
    # check parameters
    if n_iter is None:
        n = -1
    elif n_iter <= 0:
        raise ValueError("n_iter must be > 0")
    else:
        n = n_iter

    # check that we have a 2d binary image, and convert it
    # to uint8
    im = np.array(image).astype(np.uint8)

    if im.ndim != 2:
        raise ValueError("2D array required")
    if not np.all(np.in1d(image.flat, (0, 1))):
        raise ValueError("Image contains values other than 0 and 1")

    # iterate either 1) indefinitely or 2) up to iteration limit
    while n != 0:
        before = np.sum(im)  # count points before

        # for each subiteration
        for lut in luts:
            # correlate image with neighborhood mask
            N = ndi.correlate(im, LUT_DEL_MASK, mode="constant", cval=padding)
            # take deletion decision from this subiteration's LUT
            D = np.take(lut, N)
            # perform deletion
            im[D] = 0

        after = np.sum(im)  # count points after

        if before == after:
            # iteration had no effect: finish
            break

        # count down to iteration limit (or endlessly negative)
        n -= 1

    return im.astype(np.bool)


# lookup tables for thin

dil_LUT = np.array(
    [
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ],
    dtype=np.bool,
)


SPUR_LUT = np.array(
    [
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
    dtype=np.bool,
)

EP_LUT = np.array(
    [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        0,
    ],
    dtype=np.bool,
)


def spur(image, n_iter=None):
    """
      Removes "spurs" from an image

      Parameters
      ----------
      image : binary (M, N) ndarray
          The image to be spurred.

      n_iter : int, number of iterations, optional
          Regardless of the value of this parameter, the de-spurred image
          is returned immediately if an iteration produces no change.
          If this parameter is specified it thus sets an upper bound on
          the number of iterations performed.

      Returns
      -------
      out : ndarray of bools
          de-spurred image.


      Examples

      --------
    >>> t = np.array([[0, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [1, 1, 0, 0]])
    >>> spur(t).astype(np.uint8)
        array([[0 0 0 0]
               [0 0 0 0]
               [0 1 0 0]
               [1 1 0 0]]
    """
    return _bwmorph_luts(image, [SPUR_LUT], n_iter=n_iter, padding=1)


def _neighbors_conv(image):
    """
    Counts the neighbor pixels for each pixel of an image:
            x = [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ]
            _neighbors(x)
            [
                [0, 3, 0],
                [3, 4, 3],
                [0, 3, 0]
            ]
    :type image: numpy.ndarray
    :param image: A two-or-three dimensional image
    :return: neighbor pixels for each pixel of an image
    """
    image = image.astype(np.int)
    k = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    neighborhood_count = ndi.convolve(image, k, mode="constant", cval=1)
    neighborhood_count[~image.astype(np.bool)] = 0
    return neighborhood_count


def branches(image):
    """
    Returns the nodes in between edges

    Parameters
    ----------
    image : binary (M, N) ndarray

    Returns
    -------
    out : ndarray of bools
        image.

    """
    return _neighbors_conv(image) > 2


def endpointsT(image):
    """
    Returns the endpoints in an image

    Parameters
    ----------
    image : binary (M, N) ndarray

    Returns
    -------
    out : ndarray of bools
        image.

    """
    return _neighbors_conv(image) == 1


# here's how to make the LUTs


lut = np.array


def nabe(n):
    return np.array([n >> i & 1 for i in range(0, 9)]).astype(np.bool)


def hood(n):
    return np.take(nabe(n), np.array([[3, 2, 1], [4, 8, 0], [5, 6, 7]]))


def G1(n):
    s = 0
    bits = nabe(n)
    for i in (0, 2, 4, 6):
        if not (bits[i]) and (bits[i + 1] or bits[(i + 2) % 8]):
            s += 1
    return s == 1


g1_lut = np.array([G1(n) for n in range(256)])


def G2(n):
    n1, n2 = 0, 0
    bits = nabe(n)
    for k in (1, 3, 5, 7):
        if bits[k] or bits[k - 1]:
            n1 += 1
        if bits[k] or bits[(k + 1) % 8]:
            n2 += 1
    return min(n1, n2) in [2, 3]


g2_lut = np.array([G2(n) for n in range(256)])

g12_lut = g1_lut & g2_lut


def G3(n):
    bits = nabe(n)
    return not ((bits[1] or bits[2] or not (bits[7])) and bits[0])


def G3p(n):
    bits = nabe(n)
    return not ((bits[5] or bits[6] or not (bits[3])) and bits[4])


g3_lut = np.array([G3(n) for n in range(256)])
g3p_lut = np.array([G3p(n) for n in range(256)])

g123_lut = g12_lut & g3_lut
g123p_lut = g12_lut & g3p_lut


NEIGHBOR_MASK = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def too_few_neighbors(n):
    h = hood(n)
    return (h * NEIGHBOR_MASK).sum() < 2


def branchpoint_fcn(n):
    nhood = hood(n)
    if nhood[1, 1] == 1:
        count = np.sum(nhood) - 1
        if count > 2:
            return 1
        else:
            return 0
    else:
        return 0


DEL_HOOD_MAPPER = np.array([[3, 2, 1], [4, 8, 0], [5, 6, 7]])


def hood2lu(hood, lut_mask=LUT_DEL_MASK):
    return (hood * lut_mask).sum()
