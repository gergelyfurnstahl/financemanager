import csv
import re
from CategoryRegex import CategoryRegex
from OTPBankHistoryParser import OTPBankHistoryParser
import json
from ExtendedJSONSerializer import ExtendedJSONSerializer


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

def test(files):
    category_regex_dict = CategoryRegex.read_json_regex_dict('category_dict.json')
    for file in files:
        parser = OTPBankHistoryParser(category_regex_dict)
        parser.parse_bank_history(file)
        parser.print()

def main():
    category_regex_list = readData()
    category_regex_list["Unknown"] = []
    category_comments = category_init(category_regex_list)
    category_sum = sum_init(category_regex_list)
    unknown_sum = {}
    monthly_sum = 0
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
        "C:/work/financemanager/data/201911.csv"
    ]

    allfiles = aimotivefiles
    allfiles.extend(joblessfiles)
    allfiles.extend(ibkrfiles)

    currentfiles = allfiles

    test(currentfiles)
    for filename in currentfiles:

        month_category_sum = sum_init(category_regex_list)

        with open(filename) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if int(row["Amount"]) < 0:
                    found = False
                    for category, regex_list in category_regex_list.items():
                        for regex in regex_list:
                            if re.search(regex, row["Comment"]):
                                found = True
                                category_comments[category].append(row["Comment"])
                                month_category_sum[category] += int(row["Amount"])
                                break
                    if not found:
                        category_comments["Unknown"].append(row["Comment"])
                        month_category_sum["Unknown"] += int(row["Amount"])
                        if row["Comment"] not in unknown_sum:
                            unknown_sum[row["Comment"]] = 0
                        unknown_sum[row["Comment"]] += int(row["Amount"])

        monthly_sum = 0
        for val in month_category_sum.values():
            monthly_sum += val
        print(filename.split("/")[-1]+" month: " + monthly_sum.__str__() + " : " + month_category_sum.__str__())
        for key, value in month_category_sum.items():
            category_sum[key] += value

    average = "average    month: "
    averagetmp = ""
    averagesum = 0
    for key, value in category_sum.items():
        averagesum += int(value/len(currentfiles))
        averagetmp += "'" + key+"': "+int(value/len(currentfiles)).__str__()+", "
    average += averagesum.__str__() + " : {" + averagetmp[:-2] + '}'
    print(average)
    print("Sum        month: " + category_sum.__str__())
#    for key, value in category_comments.items():
#        print(key)
#        for v in value:
#            print(v)
    unknown_keys = []
    unknown_values = []
    for key, value in unknown_sum.items():
        unknown_keys.append(key)
        unknown_values.append(value)
    for money in sorted(unknown_values):
        id = unknown_values.index(money)
        print(unknown_keys[id] + " : " + unknown_values[id].__str__())
#    print(other_sum)

main()
