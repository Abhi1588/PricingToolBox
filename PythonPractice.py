import pandas as pd
import numpy as np
import matplotlib as mat

### 1. Generate a random 20x20 grid of two digit natural numbers. Find the largest product of four diagnoally
# adjacent numbers.

a = np.random.randint(10,99,(20,20))

def largest_product(a):
    prd = 0
#    d = dict()
    for row in np.arange(0,a.shape[0]-3):
        for col in np.arange(0,a.shape[0]-3):
            temp = a[row,col]*a[row+1,col+1]*a[row+2,col+2]*a[row+3,col+3]
            if temp > prd:
                prd == temp
            print(f"current max product {prd}, at row {row} and col {col}")




