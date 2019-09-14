""" Customer Relationship Management (CRM) module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * email (string)
    * subscribed (int): Is she/he subscribed to the newsletter? 1/0 = yes/no
"""

# everything you'll need is imported:
import ui
import data_manager
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
        file_name = "crm/customers.csv"
        crm_table = data_manager.get_table_from_file(file_name)
        handle_menu()
        try:
            should_exit = choose(crm_table, file_name)
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
            id_of_the_longest_name = get_longest_name_id(table)
            ui.print_result(id_of_the_longest_name, "The ID of the person with the longest name")

        elif option == "6":
            subscribers = get_subscribed_emails(table)
            ui.print_result(subscribers, "Customers subscribed to newsletter")

        elif option == "0":
            return True

    else:
        raise KeyError("There is no such option.")


def handle_menu():
    options = ["Show table",
               "Add item",
               "Remove item",
               "Update table",
               "What is the id of the customer with the longest name?",
               "Which customers has subscribed to the newsletter?"]

    ui.print_menu("Customer Relationship Management (CRM) menu", options, "Back to the main menu")


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """

    ui.print_table(table, ["ID", "NAME", "E-MAIL", "SUBSCRIPTED"])


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    inputs = ui.get_inputs(["Name: ", "E-mail: ", "Subscribed: "], "Add item")
    name, email, subscripted = inputs
    id_ = common.generate_random(table)
    table.append([id_, name, email, subscripted])
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
    titles_sales = ["Name: ", "E-mail: ", "Subscribed: "]
    inputs = ui.get_inputs(titles_sales, "Specify new properties")
    for index, item in enumerate(table):
        if id_ == item[ID]:
            table[index] = inputs
            table[index].insert(0, id_)
    return table


def get_longest_name_id(table):
    """
        Question: What is the id of the customer with the longest name?

        Args:
            table (list): data table to work on

        Returns:
            string: id of the longest name (if there are more than one, return
                the last by alphabetical order of the names)
        """
    ID = 0
    NAME = 1
    max_len = max(len(customer[NAME]) for customer in table)

    customers_with_longest_name = []
    for index in range(len(table)):
        if len(table[index][NAME]) == max_len:
            customers_with_longest_name.append(table[index][NAME])
    the_last_by_alphabet_with_longest_name = sorted_manual(customers_with_longest_name)[-1]
    for customer in table:
        if customer[NAME] == the_last_by_alphabet_with_longest_name:
            return customer[ID]


def get_subscribed_emails(table):
    """
        Question: Which customers has subscribed to the newsletter?

        Args:
            table (list): data table to work on

        Returns:
            list: list of strings (where a string is like "email;name")
        """

    NAME = 1
    EMAIL = 2
    SUBS = 3
    subscribed_to_news = []
    for customer in table:
        if int(customer[SUBS]):
            email_and_name = customer[EMAIL] + ";" + customer[NAME]
            subscribed_to_news.append(email_and_name)
    return subscribed_to_news


def sorted_manual(a_list):
    for i in range(len(a_list)):
        for j in range(i + 1, len(a_list)):
            if a_list[i] > a_list[j]:
                a_list[i], a_list[j] = a_list[j], a_list[i]
    return a_list


# functions supports data analyser
# --------------------------------


def get_name_by_id(id_):  # Eszti
    """
    Reads the table with the help of the data_manager module.
    Returns the name (str) of the customer with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the customer

    Returns:
        str: the name of the customer
    """
    table = data_manager.get_table_from_file("crm/customers.csv")
    customer_name = get_name_by_id_from_table(table, id_)
    return customer_name


def get_name_by_id_from_table(table, id_):  # Eszti
    """
    Returns the name (str) of the customer with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the customer table
        id (str): the id of the customer

    Returns:
        str: the name of the customer
    """
    ID = 0
    NAME = 1
    for customer in table:
        if customer[ID] == id_:
            return customer[NAME]
