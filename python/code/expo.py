#
# This script defines a function that raises x to the power of y
#
# This will be slower than Python's built in x**y notation or the equivalent pow function
#


def expo(x,y):
    exp = x
    for mult in range(1,y):
        exp *= x
    return exp
