""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
    * customer_id (string): id from the crm
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
        file_name = 'sales/sales.csv'
        sales_table = data_manager.get_table_from_file(file_name)
        handle_menu()
        try:
            should_exit = choose(sales_table, file_name)
            if should_exit:
                break
        except KeyError as err:
            ui.print_error_message(str(err))


def choose(table, file_name):
    inputs = ui.get_inputs(["Please enter a number: "], "")
    choice = inputs[0]
    LENGTH_OF_MENU = 7
    if choice in [str(i) for i in range(LENGTH_OF_MENU)]:
        if choice == '1':
            show_table(table)
        elif choice == '2':
            new_table = add(table)
            data_manager.write_table_to_file(file_name, new_table)
        elif choice == '3':
            input_list = ui.get_inputs(["ID: "], "Remove an item")
            id_ = input_list[0]
            try:
                new_table = remove(table, id_)
                data_manager.write_table_to_file(file_name, new_table)
            except IndexError as err:
                ui.print_error_message(str(err))
        elif choice == '4':
            input_list = ui.get_inputs(["ID: "], "Update an item")
            id_ = input_list[0]
            try:
                updated_table = update(table, id_)
                data_manager.write_table_to_file(file_name, updated_table)
            except ValueError as err:
                ui.print_error_message(str(err))
        elif choice == '5':
            result = get_lowest_price_item_id(table)
            ui.print_result(result, 'ID of the lowest price item')
        elif choice == '6':
            input_list = ["Start month: ", "Start day: ", "Start year: ", "End month: ", "End day: ", "End year: "]
            input_dates = ui.get_inputs(input_list, 'Please provide the start and end dates!')
            input_dates = [int(item) for item in input_dates]
            try:
                items = get_items_sold_between(table, *input_dates)
                show_table(items)
            except ValueError as err:
                ui.print_error_message(str(err))
        elif choice == '0':
            return True
    else:
        raise KeyError("There is no such option.")
    return False


def handle_menu():
    options = ['Show table', 'Add to table',
               'Remove from table', 'Update table',
               'Lowest price item', 'Browse items by date']

    ui.print_menu("Sales menu", options, "Back to the main menu")


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """
    titles_sales = ['id', 'title', 'price', 'month', 'day', 'year', "customer id"]
    ui.print_table(table, titles_sales)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """
    titles_sales = ['Title: ', 'Price: ', 'Month: ', 'Day: ', 'Year: ', 'Customer ID: ']
    inputs = ui.get_inputs(titles_sales, 'Please provide info about the game you wish to add.')
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
        table (list): list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """
    ID = 0
    ids = [item[ID] for item in table]
    if id_ not in ids:
        raise ValueError("The given ID not in the table.")
    titles_sales = ['Title: ', 'Price: ', 'Month: ', 'Day: ', 'Year: ', 'Customer ID: ']
    inputs = ui.get_inputs(titles_sales, "Specify new properties")
    for index, item in enumerate(table):
        if id_ == item[ID]:
            table[index] = inputs
            table[index].insert(0, id_)
    return table


# special functions:
# ------------------

def get_lowest_price_item_id(table):
    """
    Question: What is the id of the item that was sold for the lowest price?
    if there are more than one item at the lowest price, return the last item by alphabetical order of the title

    Args:
        table (list): data table to work on

    Returns:
         string: id
    """
    ID = 0
    TITLE = 1
    SOLD = 2
    id = [item[ID] for item in table]
    title = [item[TITLE] for item in table]
    units_sold = [item[SOLD] for item in table]
    lowest_sold = (id[0], title[0], units_sold[0])
    for id_, title_, units_sold_ in zip(id, title, units_sold):
        if units_sold_ < lowest_sold[SOLD]:
            if title_ < lowest_sold[TITLE]:
                lowest_sold = (id_, title_, units_sold_)
    return lowest_sold[ID]


def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)

    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)

    Returns:
        list: list of lists (the filtered table)
    """
    MONTH = 3
    DAY = 4
    YEAR = 5
    items_in_the_interval = []
    min_date = (year_from, month_from, day_from)
    max_date = (year_to, month_to, day_to)
    if min_date > max_date:
        raise ValueError("Minimum date is greater than maximum date.")
    for sale in table:
        copy_sale = sale[:]
        for index in range(len(copy_sale)):
            try:
                copy_sale[index] = int(copy_sale[index])
            except ValueError:
                pass
        sale_date = (copy_sale[YEAR], copy_sale[MONTH], copy_sale[DAY])
        if min_date < sale_date and sale_date < max_date:
            items_in_the_interval.append(copy_sale)
    if items_in_the_interval == []:
        raise ValueError("There is no item in this interval.")
    return items_in_the_interval


# functions supports data analyser
# --------------------------------

# Max
def get_title_by_id(id_):

    """
    Reads the table with the help of the data_manager module.
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the item

    Returns:
        str: the title of the item
    """
    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    title_by_id = get_title_by_id_from_table(sales_table, id_)
    return title_by_id


def get_title_by_id_from_table(table, id):  # Max

    """
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the sales table
        id (str): the id of the item

    Returns:
        str: the title of the item
    """
    ID = 0
    TITLE = 1
    for rows in table:
        if rows[ID] == id:
            return rows[TITLE]


def get_item_id_sold_last():  # Max
    """
    Reads the table with the help of the data_manager module.
    Returns the _id_ of the item that was sold most recently.
    Returns:
        str: the _id_ of the item that was sold most recently.
    """
    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    latest_sold_item = get_item_id_sold_last_from_table(sales_table)
    return latest_sold_item


def get_item_id_sold_last_from_table(table):  # Max
    """
    Returns the _id_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _id_ of the item that was sold most recently.
    """

    dates = []
    YEAR = 5
    MONTH = 3
    DAY = 4
    INDEX_MAX = 0
    for element in table:
        item = (int(element[YEAR]), int(element[MONTH]), int(element[DAY]))
        dates.append(item)
    MAX_DATE = dates[0]
    for index, date in enumerate(dates):
        if date > MAX_DATE:
            MAX_DATE = date
            INDEX_MAX = index
    return table[INDEX_MAX][0]


def get_item_title_sold_last_from_table(table):  # Évi
    """
    Returns the _title_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _title_ of the item that was sold most recently.
    """
    dates = []
    YEAR = 5
    MONTH = 3
    DAY = 4
    INDEX_MAX = 0
    for element in table:
        item = (int(element[YEAR]), int(element[MONTH]), int(element[DAY]))
        dates.append(item)
    MAX_DATE = dates[0]
    for index, date in enumerate(dates):
        if date > MAX_DATE:
            MAX_DATE = date
            INDEX_MAX = index
    return table[INDEX_MAX][1]


def get_the_sum_of_prices(item_ids):  # Évi
    """
    Reads the table of sales with the help of the data_manager module.
    Returns the sum of the prices of the items in the item_ids.

    Args:
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """
    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    sum_of_prices = get_the_sum_of_prices_from_table(sales_table, item_ids)
    return sum_of_prices


def get_the_sum_of_prices_from_table(table, item_ids):  # Évi
    """
    Returns the sum of the prices of the items in the item_ids.

    Args:
        table (list of lists): the sales table
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """
    ID = 0
    PRICE = 2
    sum_prices = 0
    for item in table:
        if item[ID] in item_ids:
            sum_prices += int(item[PRICE])
    return sum_prices


def get_customer_id_by_sale_id(sale_id):   # Évi
    """
    Reads the sales table with the help of the data_manager module.
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
         sale_id (str): sale id to search for
    Returns:
         str: customer_id that belongs to the given sale id
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    customer_id_by_sale_id = get_customer_id_by_sale_id_from_table(sales_table, sale_id)
    return customer_id_by_sale_id


def get_customer_id_by_sale_id_from_table(table, sale_id):  # Évi
    """
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
        table: table to remove a record from
        sale_id (str): sale id to search for
    Returns:
        str: customer_id that belongs to the given sale id
    """
    ID = 0
    CUSTOMER_ID = 6
    for rows in table:
        if rows[ID] == sale_id:
            return rows[CUSTOMER_ID]


def get_all_customer_ids():  # Eszti
    """
    Reads the sales table with the help of the data_manager module.

    Returns:
         set of str: set of customer_ids that are present in the table
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    customer_ids = get_all_customer_ids_from_table(sales_table)
    return customer_ids


def get_all_customer_ids_from_table(table):   # Eszti
    """
    Returns a set of customer_ids that are present in the table.

    Args:
        table (list of list): the sales table
    Returns:
         set of str: set of customer_ids that are present in the table
    """

    CUSTOMER_ID = 6
    customer_ids = {row[CUSTOMER_ID] for row in table}
    return customer_ids


def get_all_sales_ids_for_customer_ids():  # Eszti
    """
    Reads the customer-sales association table with the help of the data_manager module.
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)

    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
            all the sales id belong to the given customer_id
    """
    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    sales_ids_to_customer_id = get_all_sales_ids_for_customer_ids_from_table(sales_table)
    return sales_ids_to_customer_id


def get_all_sales_ids_for_customer_ids_from_table(table):   # Eszti
    """
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:

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

        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)
    Args:
        table (list of list): the sales table
    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
         all the sales id belong to the given customer_id
    """
    CUSTOMER_ID = 6
    SALES_ID = 0
    sales_ids_to_customer_id = {row[CUSTOMER_ID]: [] for row in table}
    for row in table:
        sales_ids_to_customer_id[row[CUSTOMER_ID]].append(row[SALES_ID])
    return sales_ids_to_customer_id


def get_num_of_sales_per_customer_ids():  # Max
    """
     Reads the customer-sales association table with the help of the data_manager module.
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """

    sales_table = data_manager.get_table_from_file("sales/sales.csv")
    sales_per_customer = get_num_of_sales_per_customer_ids_from_table(sales_table)
    return sales_per_customer


def get_num_of_sales_per_customer_ids_from_table(table):  # Max
    """
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Args:
        table (list of list): the sales table
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """
    CUST_ID = 6
    ids = []
    sales_per_customer = {}
    [ids.append(items[CUST_ID]) for items in table]
    for id in ids:
        item = {id: common.count_one_element(ids, id)}
        sales_per_customer.update(item)
    return sales_per_customer
