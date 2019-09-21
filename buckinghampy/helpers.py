import numpy as np

def tryInt(num, crit=6):
    """Cast a float as an int, but only if it makes sense.

    If the number is equal to a whole number to X decimal places, cast it as an int.

    Args:
      num (float): Number to be tested.
      crit (int): Number of decimal places to check.
    Returns:
      num as float or int

    """
    if (np.round(num, crit) % 1 == 0):
        return int(np.round(num,crit))
    else:
        return num


def isWholeNum(arr, crit=6):
    """Requires numpy array input."""
    return (np.round(arr, crit) % 1 == 0)
