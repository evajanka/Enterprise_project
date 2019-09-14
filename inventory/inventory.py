""" Inventory module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string): Name of item
    * manufacturer (string)
    * purchase_year (number): Year of purchase
    * durability (number): Years it can be used
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
        file_name = "inventory/inventory.csv"
        inventory_table = data_manager.get_table_from_file(file_name)
        handle_menu()
        try:
            should_exit = choose(inventory_table, file_name)
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
            input_list = ui.get_inputs(["ID: "], "Remove an item")
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
            avialable_items = get_available_items(table)
            ui.print_result(avialable_items, "Avialable products")
        elif option == "6":
            average_durability_by_manufacturers = get_average_durability_by_manufacturers(table)
            ui.print_result(average_durability_by_manufacturers, "Average durability times of manufacturers")
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
               "Which items have not exceeded their durability yet?",
               "What are the average durability times for each manufacturer?"]

    ui.print_menu("Inventory menu", options, "Back to the main menu")


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """

    # your code
    ui.print_table(table, ["ID", "PRODUCT", "MANUFACTURER", "RELEASE DATE", "DURABILITY"])


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    # your code
    inventory_data = ["Product: ", "Manufacturer: ", "Purchase Year: ", "Durability: "]
    inputs = ui.get_inputs(inventory_data, "Add item")
    ID = common.generate_random(table)
    table.append([ID, *inputs])
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

    # your code
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

    # your code

    ID = 0
    ids = [item[ID] for item in table]
    if id_ not in ids:
        raise ValueError("The given ID not in the table.")
    inventory_data = ["Product: ", "Manufacturer: ", "Release date: ", "Durability: "]
    inputs = ui.get_inputs(inventory_data, "Specify new properties")
    for index, item in enumerate(table):
        if id_ == item[ID]:
            table[index] = inputs
            table[index].insert(0, id_)
    return table


# special functions:
# ------------------

def get_available_items(table):
    """
    Question: Which items have not exceeded their durability yet?

    Args:
        table (list): data table to work on

    Returns:
        list: list of lists (the inner list contains the whole row with their actual data types)
    """
    expiration_date = 0
    release_date = 3
    result_list = []
    durability_yr = 4
    for rows in table:
        expiration_date = int(rows[release_date])+int(rows[durability_yr])
        if expiration_date >= 2016:
            result_list.append(rows)

    for item in result_list:
        item[release_date] = int(item[release_date])
        item[durability_yr] = int(item[durability_yr])

    return result_list


def get_average_durability_by_manufacturers(table):
    """
    Question: What are the average durability times for each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
        dict: a dictionary with this structure: { [manufacturer] : [avg] }
    """
    dict_table = {}
    MANUFACTURER = 2
    DURABILITY = 4
    for rows in table:
        dict_table.setdefault(rows[MANUFACTURER], []).append(int(rows[DURABILITY]))
    result = {key: common.sum_unique(values)/len(values) for key, values in dict_table.items()}
    return(result)
    # your code
