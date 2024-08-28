import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import re
import os
import sys
from tabulate import tabulate
from rich import print


def promt_user(id):
    match id:
        case 1:
            a = write_initValue(initialValue())
            return a
        case 4:
            a = save_solution("rungekutta4")
            print(open_csv_file("solution_rungekutta4.csv"))
        case 5:
            a = save_solution("euler")
            print(open_csv_file("solution_euler.csv"))
        case 8:
            name = str(input("Name of method: "))
            match name:
                case "euler":
                    plot_solution("solution_euler.csv")
                case "rk4":
                    plot_solution("solution_rungekutta4.csv")
                case "solution":
                    plot_solution("solution.csv")
                case _:
                    print("Comming soon")
        case 9:
            a = save_solution("solution")
        case _:
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


def true_solution_function(t):
    return float(np.tan(t))


def true_solution(f, tspan, y0, h):
    t = np.arange(tspan[0], tspan[1] + h, h)
    y = np.zeros(len(t))
    y[0] = y0

    for n in range(len(t)):
        y[n] = f(t[n])

    return t, y


def local_error(epsilon):
    return float(epsilon)


# Create ODE function
# name = input("Input the function f(t,y): ").replace("^", "**")
def ode_function(t, y):
    """Define an initial value problem (mean the problem function for eg: y'=t*y)

    Args:
        t (float): Time variables
        y (float): Dependent variables

    Returns:
        _float_: _description_
    """
    # Input is obeyed by the rule y' = f(t,y). Just only need input the f(t,y)
    f = lambda t, y: eval(sys.argv[1].replace("^", "**").replace(" ", ""))
    return f(t, y)


def tspan_init(args):
    """_summary_
    Input the string for eg [1,2], return a tuple type.
    Args:
        args (_type_): _description_

    Returns:
        tuple: _description_
    """
    pattern = re.sub(r"[\([{})\]]", "", args)
    t0, tend = pattern.split(",")
    return float(t0), float(tend)


def y0_init():
    y0 = float(input("Input the y0: "))
    return y0


def hstep():
    h = float(input("Input the step: "))
    return h


# Solvers
def euler_method(f, tn, yn, h):
    return yn + h * f(tn, yn)


def rk4_method(f, tn, yn, h):
    k1 = f(tn, yn)
    k2 = f(tn + 0.5 * h, yn + 0.5 * h * k1)
    k3 = f(tn + 0.5 * h, yn + 0.5 * h * k2)
    k4 = f(tn + h, yn + h * k3)
    return yn + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def bisection_method(f, tn, yn, h):
    pass


# Solve the ODE function
def solveODEs(f, tspan, y0, h, solver):
    """_summary_

    Args:
        f (type): is the init function that we need calculation
        tspan (list): Is the interval of t from t0 to tend
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


def save_solution(name):

    match name:
        case "euler":
            solver = euler_method
            namefile = "solution_" + name + ".csv"

            t, y = solveODEs(ode_function, tspan_init(input("Input the interval of t (eg: [0,1]): ")), y0_init(), hstep(), solver)
            with open(namefile, "w", newline="") as writefile:
                header = ["t", "y"]
                writer = csv.DictWriter(writefile, fieldnames=header)
                writer.writeheader()
                for i in range(len(t)):
                    writer.writerow({"t": f"{float(t[i]):2.3f}", "y": f"{float(y[i])}"})

        case "solution":
            namefile = name + ".csv"
            t, y = true_solution(true_solution_function, tspan_init(input("Input the interval of t (eg: [0,1]): ")), y0_init(), hstep())
            with open(namefile, "w", newline="") as writefile:
                header = ["t", "y"]
                writer = csv.DictWriter(writefile, fieldnames=header)
                writer.writeheader()
                for i in range(len(t)):
                    writer.writerow({"t": f"{float(t[i]):2.3f}", "y": f"{float(y[i])}"})
        case "rungekutta4":
            solver = rk4_method
            namefile = "solution_" + name + ".csv"
            t, y = solveODEs(ode_function, tspan_init(input("Input the interval of t (eg: [0,1]): ")), y0_init(), hstep(), solver)
            with open(namefile, "w", newline="") as writefile:
                header = ["t", "y"]
                writer = csv.DictWriter(writefile, fieldnames=header)
                writer.writeheader()
                for i in range(len(t)):
                    writer.writerow({"t": f"{float(t[i]):2.3f}", "y": f"{float(y[i])}"})
        case _:
            print("Comming soon!")


def main():
    if len(sys.argv) <= 50:
        print(open_csv_file("menu.csv"))
        promt_user(int(input("Input the ID: ")))
    elif len(sys.argv) >= 100:
        sys.exit("Too many command-line arguments")


if __name__ == "__main__":
    main()
