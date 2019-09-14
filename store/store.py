""" Store module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game
    * manufacturer (string)
    * price (number): Price in dollars
    * in_stock (number)
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
        file_name = "store/games.csv"
        store_table = data_manager.get_table_from_file(file_name)
        handle_menu()
        try:
            should_exit = choose(store_table, file_name)
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
            avl_games_by_manufacturer = get_counts_by_manufacturers(table)
            ui.print_result(avl_games_by_manufacturer, "Available number of games for each manufacturer")
        elif option == "6":
            try:
                user_input = ui.get_inputs(["Manufacturer: "], "")
                manufacturer = user_input[0]
                avg_by_manufacturer = get_average_by_manufacturer(table, manufacturer)
                ui.print_result(avg_by_manufacturer, "Average amount of games in stock")
            except KeyError:
                ui.print_error_message("Manufacturer not found.")
        elif option == "0":
            return True
    else:
        raise KeyError("There is no such option.")


def handle_menu():
    options = ["Show table",
               "Add item",
               "Remove item",
               "Update table",
               "How many different kinds of game are available of each manufacturer?",
               "What is the average amount of games in stock of a given manufacturer?"]

    ui.print_menu("Store menu", options, "Back to the main menu")
    # your code


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """
    ui.print_table(table, ["ID", "TITLE", "MANUFACTURER", "PRICE", "IN STOCK"])
    # your code


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """
    store_data = ["Title: ", "Manufacturer: ", "Price: ", "In Stock: "]
    inputs = ui.get_inputs(store_data, "Add item")
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
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """

    # your code
    ID = 0
    ids = [item[ID] for item in table]
    if id_ not in ids:
        raise ValueError("The given ID not in the table.")
    store_data = ["Title: ", "Manufacturer: ", "Price: ", "In Stock: "]
    inputs = ui.get_inputs(store_data, "Specify new properties")
    for index, item in enumerate(table):
        if id_ == item[ID]:
            table[index] = inputs
            table[index].insert(0, id_)
    return table


# special functions:
# ------------------

def get_counts_by_manufacturers(table):
    """
    Question: How many different kinds of game are available of each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
         dict: A dictionary with this structure: { [manufacturer] : [count] }
    """

    # your code
    dict_table = {}
    MANUFACTURER = 2
    TITLE = 1
    for rows in table:
        dict_table.setdefault(rows[MANUFACTURER], []).append(str(rows[TITLE]))
    result = {key: len(values) for key, values in dict_table.items()}
    return(result)


def get_average_by_manufacturer(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """
    dict_table = {}
    MANUFACTURER = 2
    IN_STOCK = 4
    for rows in table:
        dict_table.setdefault(rows[MANUFACTURER], []).append(int(rows[IN_STOCK]))
    result = {key: common.sum_unique(values)/len(values) for key, values in dict_table.items()}
    return(result[manufacturer])
