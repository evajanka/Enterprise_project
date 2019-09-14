""" Accounting module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * month (number): Month of the transaction
    * day (number): Day of the transaction
    * year (number): Year of the transaction
    * type (string): in = income, out = outflow
    * amount (int): amount of transaction in USD
"""

# everything you'll need is imported:
# # User interface module
import ui
# # data manager module
import data_manager
# # common module
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
        file_name = "accounting/items.csv"
        handle_menu()
        accounting_table = data_manager.get_table_from_file(file_name)
        try:
            should_exit = choose(accounting_table, file_name)
            if should_exit:
                break
        except KeyError as err:
            ui.print_error_message(str(err))


def choose(table, file_name):
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    LENGTH_OF_MENU = 7
    accounting_table = data_manager.get_table_from_file(file_name)
    if option in [str(i) for i in range(LENGTH_OF_MENU)]:
        if option == "1":
            show_table(accounting_table)
        if option == "2":
            data_manager.write_table_to_file(file_name, add(accounting_table))
        elif option == "3":
            input_list = ui.get_inputs(["ID: "], "Remove an item")
            id_ = input_list[0]
            try:
                new_table = remove(accounting_table, id_)
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
            max_year_profit = which_year_max(accounting_table)
            ui.print_result(max_year_profit, "Year of highest averge profit")
        elif option == "6":
            inputs = ui.get_inputs(["Year: "], "Please add the desired year:")
            year = inputs[0]
            try:
                avg_prof_yr = avg_amount(accounting_table, year)
                ui.print_result(avg_prof_yr, "Averge profit per year")
            except ZeroDivisionError:
                ui.print_error_message("Year not found.")
        elif option == "0":
            return True
    else:
        raise KeyError("There is no such option.")


def handle_menu():

    options = [
        "Show Table",
        "Add to table",
        "Remove from table",
        "Update table",
        "Year of higest profit",
        "Averge profit"]
    ui.print_menu("Accounting menu", options, "Back to main menu")


def show_table(table):

    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """
    title_list = ["id", "month", "day", "year", "type", "amount"]
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    inputs = ui.get_inputs(["Month: ", "Day: ", "Year: ", "Type: ", "Amount: "], "Add item")
    MONTH, DAY, YEAR, TYPE, AMOUNT = inputs
    ID = common.generate_random(table)
    table.append([ID, MONTH, DAY, YEAR, TYPE, AMOUNT])
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
    titles_account = ["Month: ", "Day: ", "Year: ", "Type: ", "Amount: "]
    inputs = ui.get_inputs(titles_account, "Specify new properties")
    for index, item in enumerate(table):
        if id_ == item[ID]:
            table[index] = inputs
            table[index].insert(0, id_)
    return table

# special functions:
# ------------------


def which_year_max(table):
    """
    Question: Which year has the highest profit? (profit = in - out)

    Args:
        table (list): data table to work on

    Returns:
        number
    """
    YEAR = 3
    TRANSACTION_TYPE = 4
    AMOUNT = 5
    years_profit = {}
    for item in table:
        amount = int(item[AMOUNT])
        if item[YEAR] not in years_profit:
            years_profit[item[YEAR]] = 0
        if item[TRANSACTION_TYPE] == "in":
            years_profit[item[YEAR]] += amount
        else:
            years_profit[item[YEAR]] -= amount
    year, max_value = list(years_profit.items())[0]
    for key, value in years_profit.items():
        if value > max_value:
            year, max_value = key, value
    return int(year)


def avg_amount(table, year):
    """
    Question: What is the average (per item) profit in a given year? [(profit)/(items count)]

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        number
    """
    profits_per_year = 0
    count = 0
    for element in table:
        if int(element[3]) == int(year):
            if element[4] == "in":
                profits_per_year += int(element[5])
                count += 1
            elif element[4] == "out":
                profits_per_year -= int(element[5])
                count += 1
    averge_profit_per_year = profits_per_year/count
    return averge_profit_per_year
