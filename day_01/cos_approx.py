#!/usr/bin/env python
"""Space 477: Python: I

cosine approximation function
"""
__author__ = 'Ben Osler'
__email__ = 'osler.benjamin@gmail.com'

from math import factorial
from math import pi


def cos_approx(x, accuracy=10,lst=0):
    ### lst is used to determine whether you want to do the Cosine Approximation using list comprehension or using a loop, (lst = 0 defaults to using a loop) ###
    add = []
    if lst == 1:
        add = [(((-1)**n)/factorial((2*n)))*(x**(2*n)) for n in range(accuracy)]
    else:
        for n in range(accuracy): 
            temp = (-1)**n
            temp /= factorial(2*n)
            temp *= (x**(2*n))
            add.append(temp)
        
        
        #add.append((((-1)**n)/factorial((2*n)))*(x**(2*n)))
        
    return sum(add)



# Will only run if this is run from command line as opposed to imported
if __name__ == '__main__':  # main code block
    print("cos(0) = ", cos_approx(0))
    print("cos(pi) = ", cos_approx(pi))
    print("cos(2*pi) = ", cos_approx(2*pi))
    print("more accurate cos(2*pi) = ", cos_approx(2*pi, accuracy=50))
