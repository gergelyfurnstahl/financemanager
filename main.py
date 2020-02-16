import csv
import re

from PyQt5.QtWidgets import QMainWindow, QApplication

from CategoryRegex import CategoryRegex
from OTPBankHistoryParser import OTPBankHistoryParser
import json
from ExtendedJSONSerializer import ExtendedJSONSerializer
from PyQt5 import uic
from PyQt5 import *
from mainwindow import Ui_MainWindow

def saveData(data):
    with open('C:/work/financemanager/data/regex_category.txt', "w") as file:
        for key, value in data.items():
            file.write(key + '\n')
            file.write(';'.join(value) + '\n')

def readData():
    data = {}
    with open('C:/work/financemanager/data/regex_category.txt', "r") as file:
        lines = file.readlines()
        key = None
        for line in lines:
            if not key:
                key = line.strip()
            else:
                data[key] = line.strip().split(';')
                key = None
    return data

def sum_init(data_dict):
    sum_dict = {}
    for key in data_dict:
        sum_dict[key] = 0
    return sum_dict

def category_init(data_dict):
    category_dict = {}
    for key in data_dict:
        category_dict[key] = []
    return category_dict

def main():
    aimotivefiles = [
        "C:/work/financemanager/data/201811.csv",
        "C:/work/financemanager/data/201812.csv",
        "C:/work/financemanager/data/201901.csv",
        "C:/work/financemanager/data/201902.csv",
        "C:/work/financemanager/data/201903.csv",
        "C:/work/financemanager/data/201904.csv",
        "C:/work/financemanager/data/201905.csv"
    ]

    joblessfiles = [
        "C:/work/financemanager/data/201906.csv",
        "C:/work/financemanager/data/201907.csv",
        "C:/work/financemanager/data/201908.csv"
    ]

    ibkrfiles = [
        "C:/work/financemanager/data/201909.csv",
        "C:/work/financemanager/data/201910.csv",
        "C:/work/financemanager/data/201911.csv",
        "C:/work/financemanager/data/201912.csv"
    ]

    allfiles = aimotivefiles
    allfiles.extend(joblessfiles)
    allfiles.extend(ibkrfiles)

    currentfiles = ibkrfiles

    notfoundentries = []
    stats = []
    category_regex_dict = CategoryRegex.read_json_regex_dict('category_dict.json')
    categories = list(category_regex_dict.keys())
    categories.append("notfound")
    categorysums = {}
    for cat in categories:
        categorysums[cat] = 0

    for file in currentfiles:
        parser = OTPBankHistoryParser(category_regex_dict)
        parser.parse_bank_history(file)

        for category in categories:
            for Tdata in parser.sorter.category_data_dict[category]:
                categorysums[category] += Tdata.amount

        for Tdata in parser.sorter.category_data_dict["notfound"]:
            notfoundentries.append(Tdata.__str__())

    for key,val in categorysums.items():
        stats.append(key +" average: " + str(val/len(currentfiles)))
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.notfoundlist.addItems(notfoundentries)
    ui.statsList.addItems(stats)

    app.exec_()

main()
