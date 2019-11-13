import scipp as sc


def smoothdata(variable, dim=None, NPoints=3):
    """
    Function that smooths data by assigning the value of each point to the
    mean of the values from surrounding points and itself. The number of points
    to average is NPoint, which is odd so that the point itself is in the
    center of the averaged interval. If an even NPoints is given, it is
    incremented. At the ends of the interval the full number of points is not
    used, but all available within NPoints//2 is.

    Parameters
    ----------
        variable: scipp variable
            The variable which should have its values smoothed

        dim: scipp Dim
            The dimension along which values should be smoothed

        NPoints: int
            The number of points to use in the mean (odd number)
    """

    if dim is None:
        raise ValueError("smoothdata was not given a dim to smooth.")

    if NPoints < 3:
        raise ValueError("smoothdata needs NPoints of 3 or higher.")

    data_length = len(variable[dim, :].values)
    out = variable.copy()  # preallocate output variable

    hr = NPoints//2  # half range rounded down

    # Split main loop into 3 parts, start, main and end.
    for index in range(0, hr):  # Start is before reaching half range
        start_index = 0  # Always start at 0
        end_index = int(index + hr + 1)
        out[dim, index] = sc.mean(variable[dim, start_index:end_index], dim)

    for index in range(hr, data_length - hr):  # Main is the bulk of the data
        start_index = int(index - hr)
        end_index = int(index + hr + 1)
        out[dim, index] = sc.mean(variable[dim, start_index:end_index], dim)

    for index in range(data_length - hr, data_length):  # End part
        start_index = int(index - hr)
        end_index = data_length  # Always use data length as endpoint
        out[dim, index] = sc.mean(variable[dim, start_index:end_index], dim)

    return out
