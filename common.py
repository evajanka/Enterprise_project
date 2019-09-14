""" Common module
implement commonly used functions here
"""

import random
import data_manager


def generate_random(table):  # kH38Jm#&
    """
    Generates random and unique string. Used for id/key generation:
         - at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letter
         - it must be unique in the table (first value in every row is the id)

    Args:
        table (list): Data table to work on. First columns containing the keys.

    Returns:
        string: Random and unique string
    """

    KEY = 0
    keys = [item[KEY] for item in table]
    new_key = ""
    lowers = "abcdefghijklmnopqrstuvwxyz"
    uppers = lowers.upper()
    numbers = "".join(str(number) for number in range(10))
    specials = "#&@%$"

    while True:
        for key_character_type in (lowers, uppers, numbers, numbers, uppers, lowers, specials, specials):
            new_key += random.choice(key_character_type)
        if new_key not in keys:
            break

    return new_key


def get_input_valid(user_input, label):

    if label in ["Start month: ", "Month: ", "End month: "]:
        min_month = 1
        max_month = 12
        err = ValueError(f"Please enter an intiger from {min_month} to {max_month}.")
        try:
            if int(user_input) in range(min_month, max_month + 1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label in ["Start day: ", "Day: ", "End day: "]:
        min_day = 1
        max_day = 31
        err = ValueError(f"Please enter an intiger from {min_day} to {max_day}.")
        try:
            if int(user_input) in range(min_day, max_day+1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label in ["Purchase Year: ", "Year: ", "Release date: ", "Start year: ", "End year: "]:
        min_year = 2000
        max_year = 2019
        err = ValueError(f"Please enter an intiger from {min_year} to {max_year}.")
        try:
            if int(user_input) in range(min_year, max_year+1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label == "Type: ":
        user_input = user_input.lower()
        if user_input in ["in", "out"]:
            return user_input
        else:
            raise ValueError("Type can be 'in' or 'out.")

    if label == "Amount: ":
        min_amount = 1
        max_amount = 2000
        err = ValueError(f"Please enter an intiger from {min_amount} to {max_amount}.")
        try:
            if int(user_input) in range(min_amount, max_amount+1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label == "Name: ":
        name_parts = [name_part.title() for name_part in user_input.split(" ")]
        if len(name_parts) > 1 and all(len(name_part) > 2 for name_part in name_parts):
            return " ".join(name_parts)
        else:
            raise ValueError("Last name and first name(s) of name have to be min. 3 characters long.")

    if label == "E-mail: ":
        if count_one_element(user_input, "@") == 1 and count_one_element(user_input, ".") > 0:
            return user_input.lower()
        else:
            raise ValueError("E-mail should contain one '@' and min. one '.' charachters.")

    if label == "Subscribed: ":
        err = ValueError("'1' = yes, '0' = no.")
        try:
            if int(user_input) in [1, 0]:
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label == "Birth Year: ":
        min_birth_year = 1920
        max_birth_year = 2002
        err = ValueError(f"Birth year can be between {min_birth_year} - {max_birth_year}.")
        try:
            if int(user_input) in range(min_birth_year, max_birth_year+1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label == "Manufacturer: ":
        min_len = 3
        if len(user_input) >= min_len:
            return user_input
        else:
            raise ValueError(f"Name of manufacturers must be min. {min_len} characters long.")

    if label in ["Durability: ", "Number of buyers: "]:
        min_ = 1
        if label == "Durability: ":
            max_ = 10
        else:
            max_ = 100
        err = ValueError(f"Please enter an intiger from {min_} to {max_}.")
        try:
            if int(user_input) in range(min_, max_+1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label in ["Title: ", "Product: "]:
        min_len = 3
        if len(user_input) >= min_len:
            return user_input
        else:
            raise ValueError(f"Name must be min. {min_len} characters long.")

    if label == "Price: ":
        min_price = 1
        max_price = 200
        err = ValueError(f"Price can be between {min_price} - {max_price}.")
        try:
            if int(user_input) in range(min_price, max_price+1):
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    if label == "Customer ID: ":
        ID = 0
        file_name = "crm/customers.csv"
        crm_table = data_manager.get_table_from_file(file_name)
        ids = [item[ID] for item in crm_table]
        if user_input in ids:
            return user_input
        else:
            raise ValueError("The given Customer ID not in the CRM table.")

    elif label == "In Stock: ":
        err = ValueError("Please enter a non-negative intiger.")
        try:
            if int(user_input) >= 0:
                return user_input
            else:
                raise err
        except ValueError:
            raise err

    else:
        return user_input


def sum_unique(table):
    sum = 0
    for items in table:
        sum += items
    return sum


def sort_unique(my_list):
    if len(my_list) > 1:
        mid = len(my_list)//2
        first_half = sort_unique(my_list[:mid])
        second_half = sort_unique(my_list[mid:])

        first_half_index = 0
        second_half_index = 0
        mergelist_index = 0

        while first_half_index < len(first_half) and second_half_index < len(second_half):
            if first_half[first_half_index] < second_half[second_half_index]:
                my_list[mergelist_index] = first_half[first_half_index]
                first_half_index += 1
            else:
                my_list[mergelist_index] = second_half[second_half_index]
                second_half_index += 1
            mergelist_index += 1

        while first_half_index < len(first_half):
            my_list[mergelist_index] = first_half[first_half_index]
            first_half_index += 1
            mergelist_index += 1

        while second_half_index < len(second_half):
            my_list[mergelist_index] = second_half[second_half_index]
            second_half_index += 1
            mergelist_index += 1

    return my_list


def count_one_element(list_or_string, searched_element):
    counter = 0
    for element in list_or_string:
        if element == searched_element:
            counter += 1
    return counter
