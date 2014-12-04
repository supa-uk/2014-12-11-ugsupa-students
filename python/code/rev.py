#
# This defines a function that returns the reverse of a string, 
# using a loop
#
#
#


def rev(string):
    reverse_string = ''
    for c in range(len(string)-1, -1, -1):
        reverse_string += string[c]
        
    return reverse_string
