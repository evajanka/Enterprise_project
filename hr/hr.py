""" Human resources module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * birth_year (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """
    while True:
        file_name = "hr/persons.csv"
        hr_table = data_manager.get_table_from_file(file_name)
        handle_menu()
        try:
            should_exit = choose(hr_table, file_name)
            if should_exit:
                break
        except KeyError as err:
            ui.print_error_message(str(err))


def choose(table, file_name):
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    LENGTH_OF_MENU = 7

    if option in [str(i) for i in range(LENGTH_OF_MENU)]:

        if option == "1":
            show_table(table)

        elif option == "2":
            new_table = add(table)
            data_manager.write_table_to_file(file_name, new_table)

        elif option == "3":
            input_list = ui.get_inputs(["ID: "], "Remove item")
            id_ = input_list[0]
            try:
                new_table = remove(table, id_)
                data_manager.write_table_to_file(file_name, new_table)
            except IndexError as err:
                ui.print_error_message(str(err))

        elif option == "4":
            input_list = ui.get_inputs(["ID: "], "Update an item")
            id_ = input_list[0]
            try:
                updated_table = update(table, id_)
                data_manager.write_table_to_file(file_name, updated_table)
            except ValueError as err:
                ui.print_error_message(str(err))

        elif option == "5":
            oldest_persons = get_oldest_person(table)
            ui.print_result(oldest_persons, "The oldest person(s)")

        elif option == "6":
            persons_closest_to_average = get_persons_closest_to_average(table)
            ui.print_result(persons_closest_to_average, "Person(s) closest to average age")

        elif option == "0":
            return True

    else:
        raise KeyError("There is no such option.")
    return False


def handle_menu():
    options = ["Show table",
               "Add item",
               "Remove item",
               "Update table",
               "Who is the oldest person?",
               "Who is the closest to the average age?"]

    ui.print_menu("Human Resources Management Menu", options, "Back to the main menu")


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """

    ui.print_table(table, ["ID", "NAME", "BIRTH YEAR"])


def add(table):
    """
    Asks useid_he table.

    Args:
        tablid_ord to

    Returns:id_
        list: Table with a new record
    """

    inputs = ui.get_inputs(["Name: ", "Birth Year: "], "Add item")
    name, birth_year = inputs
    id_ = common.generate_random(table)
    table.append([id_, name, birth_year])
    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table (list): table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        list: Table without specified record.
    """

    ID = 0
    ids = [item[ID] for item in table]
    if id_ not in ids:
        raise IndexError("The given ID not in the table.")
    new_table = [item for item in table if item[ID] != id_]
    return new_table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table (list): list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """
    ID = 0
    ids = [item[ID] for item in table]
    if id_ not in ids:
        raise ValueError("The given ID not in the table.")
    titles_sales = ["Name: ", "Birth Year: "]
    inputs = ui.get_inputs(titles_sales, "Specify new properties")
    for index, item in enumerate(table):
        if id_ == item[ID]:
            table[index] = inputs
            table[index].insert(0, id_)
    return table


# special functions:
# ------------------

def get_oldest_person(table):
    """
    Question: Who is the oldest person?

    Args:
        table (list): data table to work on

    Returns:
        list: A list of strings (name or names if there are two more with the same value)
    """
    NAME = 1
    YEAR = 2
    year_for_max_age = min(person_data[YEAR] for person_data in table)
    oldest_persons = [person_data[NAME] for person_data in table if person_data[YEAR] == year_for_max_age]
    return oldest_persons


def get_persons_closest_to_average(table):
    """
    Question: Who is the closest to the average age?

    Args:
        table (list): data table to work on

    Returns:
        list: list of strings (name or names if there are two more with the same value)
    """

    NAME = 1
    YEAR = 2
    years = [int(person_data[YEAR]) for person_data in table]
    sum_of_years = 0  # for min difference:
    for year in years:
        sum_of_years += year
    average_year = round(sum_of_years / len(years))
    min_difference = min(abs(int(person_data[YEAR]) - average_year) for person_data in table)
    for index in range(len(table)):   # add -difference from average year- column for every person:
        difference_from_average = abs(int(table[index][YEAR]) - average_year)
        table[index].append(difference_from_average)
    DIFFERENCE = 3
    persons_age_closest_to_avr = []
    for person_data in table:
        if person_data[DIFFERENCE] == min_difference:
            persons_age_closest_to_avr.append(person_data[NAME])
    return persons_age_closest_to_avr
