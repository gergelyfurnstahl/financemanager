import re
import dataclasses


@dataclasses.dataclass
class TransactionData:
    amount: int
    comment: str
    matched_regex: str


class TransactionSorter:
    def __init__(self, category_regex_dict, notfound_category_name="notfound"):
        self.category_regex_dict = category_regex_dict
        self.not_found_category_name = notfound_category_name
        self.category_data_dict = {}
        self.category_sum_dict = {}
        for category in self.category_regex_dict:
            self.category_data_dict[category] = []
            self.category_sum_dict[category] = 0
        self.category_data_dict[self.not_found_category_name] = []
        self.category_sum_dict[self.not_found_category_name] = 0
        self.sum = 0;

    def add(self, amount, comment):
        if int(amount) >= 0:
            return
        for category, regex_list in self.category_regex_dict.items():
            for regex in regex_list:
                if re.search(regex, comment):
                    self.category_data_dict[category].append(TransactionData(amount, comment, regex))
                    self.category_sum_dict[category] += amount
                    self.sum += amount
                    return

        self.category_data_dict[self.not_found_category_name].append(TransactionData(amount, comment, self.not_found_category_name))
        self.category_sum_dict[self.not_found_category_name] += amount
        self.sum += amount
