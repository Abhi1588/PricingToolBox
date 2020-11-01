import pandas as pd
import numpy as np
import scipy.stats as stat
import matplotlib as mat
"""
Problem 1:  Generate a random 20x20 grid of two digit natural numbers. Find the largest product of four 
            diagonally adjacent numbers.
"""
a = np.random.randint(10, 99, (20, 20))

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

"""
Probelm 2:  The Social Security administration has this neat data by year of what names are most popular 
            by gender for born that year in the USA. The popular name list for the year 1990 is given in the 
            website <url>. Write a python program to identify the names that appear in the list of popular
            names of both genders. 
"""

data = pd.read_csv("popular_names.csv")

def popular_name(data):

    males = set(data['Male name'])
    females = set(data['Female name'])
    common = males.intersection(females)
    d = dict()
    for name in common:
        combined_rank = int(data['Rank'][data['Male name']== name] ) + int(data['Rank'][data['Female name']== name])
        d.update({combined_rank:name})
        #print(f"Name: {name},\t Rank: {combined_rank}")

    name = d[min(d.keys())]

    return name

print(f"Most Popular name {popular_name(data)}")

"""
Problem 3: Invert matrix using first principle
"""

#b = np.random.randint(10, 99, (3, 3))

def matrix_invert_first_principles(b):

    if b.shape[0] != b.shape[1]:
        return print("Please input a square matrix")

    b = b.astype("float")
    c = b.copy()
    I = np.eye(b.shape[0], b.shape[1])

    for i in np.arange(0, b.shape[0]):
        I[i] = I[i, :] / b[i, i]
        b[i] = b[i, :] / b[i, i]
        for j in np.arange(0, b.shape[0]):
            if j == i:
                pass
            else:
                I[j] = I[j] - b[j, i] * I[i]
                b[j] = b[j] - b[j, i] * b[i]

    def check_result(result, actual):

        res = np.matmul(result, actual).astype("int")
        #print(res)
        if (np.eye(result.shape[0], result.shape[1]) == res).all():
            ok = True
            d_res = None
        else:
            ok = False
            d_res = {"input": actual}

        return ok, d_res

    if not check_result(I, c)[0]:
        return (f"Something not ok. Input {check_result(I, c)[1]['input']}")

    return I


# b = np.array(  [[35, 40, 82],
#                 [68, 86, 29],
#                 [38, 53, 13]])

print(f"Result Problem 3: {matrix_invert_first_principles(b)}")

"""
Problem 5:  Numerical Integration using Monte Carlo simulation.

"""

def integrate_func_monte_carlo(func,a,b,N=1000):
    x = np.random.uniform(a, b, N)
    res = func(x)
    return ((b-a)/N)*sum(res)

def func0(x):
    return x

def func_a(x):
    return np.exp(-x**2)

def func_b(x):
    return 1/(1 + x**2)

def func_c(x):
    return np.sqrt(x**4 + 1)

def confidence_interval(arr, p = 0.95):

    u = arr.mean()
    sd = arr.std()
    z = stat.norm.ppf(1-(1-p)/2)

    ci = z*(sd/np.sqrt(len(arr)))
    d = {"mean": u,
         "interval":ci}
    return d

def compute_value(func,a,b,theo_vaule,N=1000):
    print(N)
    r = []
    for _ in np.arange(0,100):
        r.append(integrate_func_monte_carlo(func, a, b, N))

    result = np.array(r)
    diff_arr = result - theo_vaule
    result_dict = {"result":result}
    result_dict.update(confidence_interval(diff_arr))

    return result_dict



temp = []
l_N = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 1000000]

for N in l_N:
    de = compute_value(func0,0,1,0.5,N)
    temp.append(de)




