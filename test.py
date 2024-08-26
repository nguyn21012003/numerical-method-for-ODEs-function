import numpy as np
import matplotlib as plot
import csv
import re
import os
from tabulate import tabulate
from rich import print


def tspan_init(args):
    """_summary_
    Input the string for eg [1,2], return a tuple type.
    Args:
        args (_type_): _description_

    Returns:
        _type_: _description_
    """
    patn = re.sub(r"[\([{})\]]", "", args)
    a, b = patn.split(",")
    return float(a), float(b)


def y0_init():
    y0 = float(input("Input the y0: "))
    return y0


def hstep():
    h = float(input("Input the step: "))
    return h


def euler_method(f, tn, yn, h):
    return yn + h * f(tn, yn)


def ivp_function(t, y):
    """Define an initial value problem (mean the problem function for eg: y'=t*y)

    Args:
        t (float): _description_
        y (float): _description_

    Returns:
        _float_: _description_
    """
    return t * y


def solveODEs(f, tspan, y0, h, solver):
    """_summary_

    Args:
        f (type): _description_
        tspan (type): Is the interval of t from a to b
        y0 (float): Description
        h (float): is the step that calculate from t0 to t1. This can get from the hstep() function
        solver (type): is any solver like Euler Method or RK4 Method
    """
    t = np.arange(tspan[0], tspan[1] + h, h)
    y = np.zeros(len(t))  # Create an array with all the array[i] is zero
    y[0] = y0  # y0 is taken from y0_init() function

    for n in range(len(t) - 1):
        y[n + 1] = solver(f, t[n], y[n], h)

    return t, y


def main():
    t, y = solveODEs(ivp_function, tspan_init(str(input("Input the interval(eg: [1,2]): "))), y0_init(), hstep(), euler_method)
    print(ivp_function)


if __name__ == "__main__":
    main()
