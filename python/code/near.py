#
# This code defines a function that tests whether a first number is within 10% of the magnitude of a second number
# 
# 
#


def near(first, second):
    import numpy
    tolerance = 0.1*numpy.absolute(second)
    if numpy.absolute(first-second) <= tolerance: return True
    else: return False
    
    
    
