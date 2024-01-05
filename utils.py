# common function for retrieving a boolean value from a dictionary by group ID
def get_value(dictionary: dict, key: int):
    if key in dictionary:
        print(dictionary.get(key))
        return dictionary.get(key)
    else:
        return False


# lolo, a function for presenting the state of a feature in a user-friendly way
def transform_value(value):
    if value is False:
        return "Disabled"
    else:
        return "Enabled"


def add_to_filter(dictionary: dict, key: int, value: bool):
    dictionary[key] = value
