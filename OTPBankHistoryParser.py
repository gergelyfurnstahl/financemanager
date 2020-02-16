import csv
from TransactionSorter import TransactionSorter


class OTPBankHistoryParser:
    def __init__(self, category_regex_dict):
        self.sorter = TransactionSorter(category_regex_dict)

    def parse_bank_history(self, filename):
        with open(filename) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                self.sorter.add(int(row["Amount"]), row["Comment"])

    def print(self):
        print(str(self.sorter.sum) + " : " + self.sorter.category_sum_dict.__str__())
        for w in sorted(self.sorter.category_sum_dict, key=self.sorter.category_sum_dict.get, reverse=False):
            print(w + ": " + str(self.sorter.category_sum_dict[w]))