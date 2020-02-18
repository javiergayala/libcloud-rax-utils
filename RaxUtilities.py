"""Miscellaneous functions."""


def prRed(redStr):
    """Output text in red.

    :param strredStrk: Text to print in red
    :returns: String formatted in red
    :rtype: str

    """
    out = "\033[91m {}\033[00m".format(redStr)
    return out


def prGreen(greenStr):
    """Output text in green.

    :param str greenStr: Text to print in green
    :returns: String formatted in green
    :rtype: str
    """
    out = "\033[92m {}\033[00m".format(greenStr)
    return out
