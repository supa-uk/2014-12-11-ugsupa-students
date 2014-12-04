#
# This defines a function that returns the reverse of a string using 
# slice syntax (slicing works not just for NumPy arrays but also for
# lists and string). The slicing syntax used is [start:end:step], and
# since start and end are left unspecified the full string is traversed
#
#

def rev_fast(string):
    return string[::-1]
