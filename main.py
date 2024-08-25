import numpy as np
import matplotlib as plot
import csv
import os
from tabulate import tabulate


def promt_user(id):
    if id == 1:
        a = write_initValue(initialValue())
        return a


def menu(name):
    with open(name, "r") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            rows.append(row)
        return tabulate(rows, headers="keys", tablefmt="rounded_grid")


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


def solveODEs(arg):
    pass


def main():
    print(menu("menu.csv"))
    print(promt_user(int(input("Choose the fucntion you want: "))))


if __name__ == "__main__":
    main()
