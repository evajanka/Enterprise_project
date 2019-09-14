"""
This module creates reports for the marketing department.
This module can run independently from other modules.
Has no own data structure but uses other modules.
Avoud using the database (ie. .csv files) of other modules directly.
Use the functions of the modules instead.
"""

# importing everything you need
import ui
from sales import sales
from crm import crm


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """
    while True:
        handle_menu()
        try:
            should_exit = choose()
            if should_exit:
                break
        except KeyError as err:
            ui.print_error_message(str(err))


def choose():
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]
    LENGTH_OF_MENU = 7
    if option in [str(i) for i in range(LENGTH_OF_MENU)]:
        if option == "1":
            latest_buyer_name = get_the_last_buyer_name()
            ui.print_result(latest_buyer_name, "Name of the latest sell")
        elif option == "2":
            latest_buyer_id = get_the_last_buyer_id()
            ui.print_result(latest_buyer_id, "ID of the latest buyer")
        elif option == "3":
            name_and_amount_of_highest_purchase = get_the_buyer_name_spent_most_and_the_money_spent()
            ui.print_result(name_and_amount_of_highest_purchase, "Name and amount of the highest purchase")
        elif option == "4":
            ID_and_amount_of_highest_purchase = get_the_buyer_id_spent_most_and_the_money_spent()
            ui.print_result(ID_and_amount_of_highest_purchase, "ID and amount of the highest purcase")
        elif option == "5":
            nums = ui.get_inputs(["Number of buyers: "], "")
            number = int(nums[0])
            most_frequent_buyers = get_the_most_frequent_buyers_names(number)
            ui.print_result(most_frequent_buyers, "Name of the most frequent buyers and number of sales")
        elif option == "6":
            nums = ui.get_inputs(["Number of buyers: "], "")
            number = int(nums[0])
            ID_of_most_frequent_buyers = get_the_most_frequent_buyers_ids(number)
            ui.print_result(ID_of_most_frequent_buyers, "ID of the most frequent buyers")
        elif option == "0":
            return True
    else:
        raise KeyError("There is no such option.")


def handle_menu():

    options = [

        "Name of the latest buyer",
        "ID of the latest buyer",
        "Name and amount of highest purchase",
        "ID and amount of highest purchase",
        "Names of most frequent buyers",
        "ID-s of most frequent buyers"

        ]
    ui.print_menu("Accounting menu", options, "Back to main menu")


def get_the_last_buyer_name():  # Évi
    """
    Returns the customer _name_ of the customer made sale last.

    Returns:
        str: Customer name of the last buyer
    """
    sale_id = sales.get_item_id_sold_last()
    last_buyer_id = sales.get_customer_id_by_sale_id(sale_id)
    last_buyer_name = crm.get_name_by_id(last_buyer_id)
    return last_buyer_name


def get_the_last_buyer_id():  # Évi
    """
    Returns the customer _id_ of the customer made sale last.

    Returns:
        str: Customer id of the last buyer
    """
    sale_id = sales.get_item_id_sold_last()
    last_buyer_id = sales.get_customer_id_by_sale_id(sale_id)
    return last_buyer_id


def get_the_buyer_name_spent_most_and_the_money_spent():  # Eszti
    """
    Returns the customer's _name_ who spent the most in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer name and the sum the customer spent eg.: ('Daniele Coach', 42)
    """
    BUYER = 0
    customer_and_max_spent_money = list(get_the_buyer_id_spent_most_and_the_money_spent())
    customer_and_max_spent_money[BUYER] = crm.get_name_by_id(customer_and_max_spent_money[BUYER])
    return tuple(customer_and_max_spent_money)


def get_the_buyer_id_spent_most_and_the_money_spent():  # Eszti
    """
    Returns the customer's _id_ who spent more in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer id and the sum the customer spent eg.: (aH34Jq#&, 42)
    """
    sales_ids_to_customer_id = sales.get_all_sales_ids_for_customer_ids()
    customer_and_max_spent_money = [None, 0]
    MONEY = 1
    for customer_id, sales_ids in sales_ids_to_customer_id.items():
        sum_of_prices = sales.get_the_sum_of_prices(sales_ids)
        if sum_of_prices > customer_and_max_spent_money[MONEY]:
            customer_and_max_spent_money = [customer_id, sum_of_prices]
    return tuple(customer_and_max_spent_money)


def get_the_most_frequent_buyers_names(num=1):  # Max
    """
    Returns 'num' number of buyers (more precisely: the customer's name) who bought most frequently in an
    ordered list of tuples of customer names and the number of their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer names and num of sales
            The first one bought the most frequent. eg.: [('Genoveva Dingess', 8), ('Missy Stoney', 3)]
    """
    result_lst = []
    sales_per_customer = sales.get_num_of_sales_per_customer_ids()
    for ID, NUM_OF_PURCHASES in sales_per_customer.items():
        tuple_of_customer = ((crm.get_name_by_id(ID)), NUM_OF_PURCHASES)
        result_lst.append(tuple_of_customer)
    return result_lst[:num]


def get_the_most_frequent_buyers_ids(num=1):  # Max
    """
    Returns 'num' number of buyers (more precisely: the customer ids of them) who bought more frequent in an
    ordered list of tuples of customer id and the number their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer ids and num of sales
            The first one bought the most frequent. eg.: [(aH34Jq#&, 8), (bH34Jq#&, 3)]
    """
    result_lst = []
    sales_per_customer = sales.get_num_of_sales_per_customer_ids()
    for ID, NUM_OF_PURCHASES in sales_per_customer.items():
        tuple_of_customer = (ID, NUM_OF_PURCHASES)
        result_lst.append(tuple_of_customer)
    return result_lst[:num]
