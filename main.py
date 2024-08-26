import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import re
import os
from tabulate import tabulate
from rich import print


def promt_user(id):
    if id == 1:
        a = write_initValue(initialValue())
        return a
    elif id == 8:
        a = save_solution()
        print(open_csv_file("solution_eulermethod.csv"))
    elif id == 9:
        name = str(input("Name of method: "))
        if name == "euler":
            plot_solution("solution_eulermethod.csv")
        else:
            print("Comming soon")
    else:
        raise TypeError("TypeError")


def open_csv_file(name):
    with open(name, "r") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            rows.append(row)
        return tabulate(rows, headers="keys", tablefmt="rounded_grid")


def plot_solution(name):
    """Open file solution.csv. Then return 2 arrays, its will be t and y

    Args:
        name (string): _description_
    """
    with open(name, "r") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            rows.append(row)
    tpoints = []
    ypoints = []
    for i in range(len(rows)):
        t = rows[i]["t"]
        y = rows[i]["y"]
        tpoints.append(float(t))
        ypoints.append(float(y))

    # We can use this list comprehension:
    # tpoints.extend([float(rows[i]["t"]) for i in range(len(rows))]) or tpoints = [float(rows[i]["t"]) for i in range(len(rows))]
    # ypoints.extend([float(rows[i]["y"]) for i in range(len(rows))]) or ypoints = [float(rows[i]["y"]) for i in range(len(rows))]

    fig, ax = plt.subplots()
    plt.plot(tpoints, ypoints, "b-o")
    plt.xlabel("$t")
    plt.ylabel("$y")
    plt.show()


def initialValue():
    """_summary_

    Returns:
        _dictionaries_: return a dict that contain the keys and values
    """
    initValue = {}
    with open("initialValue.csv", "w", newline="") as writefile:
        writer = csv.DictWriter(writefile, fieldnames=["Const", "Value"])
        writer.writeheader()
        i = 0
        while True:
            try:
                const, value = input(f"Input value of x_{i}(eg: x0=1,x1=2,...): ").strip().lower().split("=")
                initValue[const] = value
                i += 1
            except EOFError as e:
                print(initValue)
                break
            except KeyboardInterrupt as kbi:
                print("\nKeyboardInterrupt")
                break
    return initValue


def write_initValue(initValue):
    """_summary_

    Args:
        initValue (Dictionaries): Get this from the function initialValue()

    Returns:
        rows: which is a List in Lists
    """
    if len(initValue) == 0:
        return f"Initial Value is empty"
    else:
        with open("initialValue.csv", "w", newline="") as writefile:
            writer = csv.writer(writefile)
            header = ["Constant", "Value"]
            writer = csv.DictWriter(writefile, fieldnames=header)
            writer.writeheader()

            for key, value in initValue.items():
                writer.writerow({"Constant": key, "Value": value})

        with open("initialValue.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = []
            for row in reader:
                rows.append(row)

            # print(rows)
            return tabulate(rows, headers="keys", tablefmt="rounded_grid")


def tspan_init(args):
    """_summary_
    Input the string for eg [1,2], return a tuple type.
    Args:
        args (_type_): _description_

    Returns:
        tuple: _description_
    """
    pattern = re.sub(r"[\([{})\]]", "", args)
    a, b = pattern.split(",")
    return float(a), float(b)


def y0_init():
    y0 = float(input("Input the y0: "))
    return y0


def hstep():
    h = float(input("Input the step: "))
    return h


def euler_method(f, tn, yn, h):
    return yn + h * f(tn, yn)


def ode_function(t, y):
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
        f (type): is the init function that we need calculation
        tspan (list): Is the interval of t from a to b
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


def save_solution():
    t, y = solveODEs(ode_function, tspan_init(input("Input the interval of t (eg: '1,2'): ")), y0_init(), hstep(), euler_method)

    with open("solution_eulermethod.csv", "w", newline="") as writefile:
        header = ["t", "y"]
        writer = csv.DictWriter(writefile, fieldnames=header)
        writer.writeheader()
        for i in range(len(t)):
            writer.writerow({"t": f"{float(t[i])}", "y": f"{float(y[i])}"})


def main():
    print(open_csv_file("menu.csv"))
    promt_user(int(input("Input the ID: ")))


if __name__ == "__main__":
    main()
