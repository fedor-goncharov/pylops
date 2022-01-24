import warnings

from numpy.core.multiarray import normalize_axis_index

from pylops.signalprocessing import ConvolveND


def Convolve2D(
    N, h, dims, offset=(0, 0), axes=(-2, -1), nodir=None, dtype="float64", method="fft"
):
    r"""2D convolution operator.

    Apply two-dimensional convolution with a compact filter to model
    (and data) along a pair of ``axes`` of a two or
    three-dimensional array.

    Parameters
    ----------
    N : :obj:`int`
        Number of samples in model
    h : :obj:`numpy.ndarray`
        2d compact filter to be convolved to input signal
    dims : :obj:`list`
        Number of samples for each dimension
    offset : :obj:`tuple`, optional
        Indices of the center of the compact filter
    axes : :obj:`int`, optional
        .. versionadded:: 2.0.0

        Axes along which convolution is applied
    nodir : :obj:`int`, optional
        Direction along which smoothing is **not** applied (set to ``None`` for 2d
        arrays)

        .. deprecated:: 2.0.0
            Use ``axes`` instead. Note that ``axes`` applies along axes instead.

    dtype : :obj:`str`, optional
        Type of elements in input array.
    method : :obj:`str`, optional
        Method used to calculate the convolution (``direct`` or ``fft``).

    Returns
    -------
    cop : :obj:`pylops.LinearOperator`
        Convolve2D linear operator

    Notes
    -----
    The Convolve2D operator applies two-dimensional convolution
    between the input signal :math:`d(t,x)` and a compact filter kernel
    :math:`h(t,x)` in forward model:

    .. math::
        y(t,x) = \iint\limits_{-\infty}^{\infty}
        h(t-\tau,x-\chi) d(\tau,\chi) \,\mathrm{d}\tau \,\mathrm{d}\chi

    This operation can be discretized as follows

    .. math::
        y[i,n] = \sum_{j=-\infty}^{\infty} \sum_{m=-\infty}^{\infty} h[i-j,n-m] d[j,m]


    as well as performed in the frequency domain.

    .. math::
        Y(f, k_x) = \mathscr{F} (h(t,x)) * \mathscr{F} (d(t,x))

    Convolve2D operator uses :py:func:`scipy.signal.convolve2d`
    that automatically chooses the best domain for the operation
    to be carried out.

    As the adjoint of convolution is correlation, Convolve2D operator
    applies correlation in the adjoint mode.

    In time domain:

    .. math::
        y(t,x) = \iint\limits_{-\infty}^{\infty}
        h(t+\tau,x+\chi) d(\tau,\chi) \,\mathrm{d}\tau \,\mathrm{d}\chi

    or in frequency domain:

    .. math::
        y(t, x) = \mathscr{F}^{-1} (H(f, k_x)^* * X(f, k_x))

    """
    if h.ndim != 2:
        raise ValueError("h must be 2-dimensional")
    if nodir is not None:
        warnings.warn(
            "nodir is deprecated in version 2.0.0, use axes instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        if nodir == 0:
            axes = (1, 2)
        elif nodir == 1:
            axes = (0, 2)
        else:
            axes = (0, 1)
    else:
        axes = tuple(normalize_axis_index(ax, len(dims)) for ax in axes)

    cop = ConvolveND(N, h, dims, offset=offset, axes=axes, method=method, dtype=dtype)
    return cop
