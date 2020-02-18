"""Miscellaneous functions."""


def prRed(skk):
    """Output text in red.

    Arguments:
        skk {str} -- text to format as red
    """
    out = "\033[91m {}\033[00m".format(skk)
    return out


def prGreen(skk):
    """Output text in green.

    Arguments:
        skk {str} -- text to format as green
    """
    out = "\033[92m {}\033[00m".format(skk)
    return out
