import pandas as pd
import numpy as np
import matplotlib as mat

### 1. Generate a random 20x20 grid of two digit natural numbers. Find the largest product of four diagnoally
# adjacent numbers.

a = np.random.randint(10,99,(20,20))

def largest_product(a):
    prd = 0
    d = dict()
    l = []
    for row in np.arange(0,a.shape[0]-3):
        for col in np.arange(0,a.shape[0]-3):
            temp_down = a[row, col]*a[row+1, col+1]*a[row+2, col+2]*a[row+3, col+3]
            temp_up = a[row+3, col]*a[row+2, col+1]*a[row+1, col+2]*a[row, col+3]
            if temp_up > temp_down:
                temp = temp_up
                address = f"Up Diag {(row+3, col),(row+2,col+1),(row+1,col+2),(row,col+3)}"
            else:
                temp = temp_down
                address = f"Down Diag {(row, col),(row+1,col+1),(row+2,col+2),(row+3,col+3)}"
            l.append([temp,temp_up,temp_down])
            if temp > prd:
                prd = temp
                d = {"product": prd,
                  "address": address}
    return d

print(f"Maximum Product: {largest_product(a)['product']} \nAddress: {largest_product(a)['address']}")

