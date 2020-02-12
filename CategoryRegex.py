import json


class CategoryRegex:

    @staticmethod
    def read_txt_regex_dict(filename):
        category_regex_dict = {}
        with open(filename, "r") as file:
            lines = file.readlines()
            key = None
            for line in lines:
                if not key:
                    key = line.strip()
                else:
                    category_regex_dict[key] = line.strip().split(';')
                    key = None
        return category_regex_dict

    @staticmethod
    def read_json_regex_dict(filename):
        category_regex_dict = {}
        with open(filename, "r") as file:
            category_regex_dict = json.load(file)
        return category_regex_dict

    @staticmethod
    def export_dict_to_json(filename, category_regex_dict):
        with open(filename, 'w') as file:
            file.write(json.dumps(category_regex_dict,  indent=4, sort_keys=True))

