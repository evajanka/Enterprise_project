""" User Interface (UI) module """


import common


def print_table(table, title_list):
    """
    Prints table with data.

    Example:
        /-----------------------------------\
        |   id   |      title     |  type   |
        |--------|----------------|---------|
        |   0    | Counter strike |    fps  |
        |--------|----------------|---------|
        |   1    |       fo       |    fps  |
        \-----------------------------------/

    Args:
        table (list): list of lists - table to display
        title_list (list): list containing table headers

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    max_len = {index: len(i) for index, i in enumerate(table[0])}
    for index, item in enumerate(title_list):
        if len(item) > max_len[index]:
            max_len[index] = len(item)
    for item in table:
        for index, feature in enumerate(item):
            if len(feature) > max_len[index]:
                max_len[index] = len(feature)
    max_len_sum = 0
    for i in max_len.values():
        max_len_sum += i
    header = '|' + '|'.join(t.lower().center(max_len[idx]) for idx, t in enumerate(title_list)) + '|'
    dash = '-' * (len(header) - len('||'))
    print(f'/{dash}\\')
    print(header)
    for index, t in enumerate(table):
        print(f'|{dash}|')
        print('|' + '|'.join(tt.center(max_len[idx]) for idx, tt in enumerate(t)) + '|')
    print(f'\\{dash}/')


def print_result(result, label):
    """
    Displays results of the special functions.

    Args:
        result: result of the special function (string, list or dict)
        label (str): label of the result

    Returns:
        None: This function doesn't return anything it only prints to console.
    """
    print(f'\n{label}:')
    if type(result) == list:
        if len(result) > 0 and type(result[0]) == list:
            for item in result:
                print('|'.join(map(str, item)))
        else:
            for item in result:
                print(f'\t{item}')
    elif type(result) == dict:
        for key, value in result.items():
            print(f'\t{key}: {value}')
    else:
        print(f'\t{result}')


def print_menu(title, list_options, exit_message):
    """
    Displays a menu. Sample output:
        Main menu:
            (1) Store manager
            (2) Human resources manager
            (3) Inventory manager
            (4) Accounting manager
            (5) Sales manager
            (6) Customer relationship management (CRM)
            (0) Exit program

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print(f'\n{title}:')
    menu = tuple(zip(range(1, len(list_options) + 1), list_options))
    for m in menu:
        print(f'\t({m[0]}) {m[1]}')
    print(f'\t(0) {exit_message}')


def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.
    Sample call:
        get_inputs(["Name","Surname","Age"],"Please provide your personal information")
    Sample display:
        Please provide your personal information
        Name <user_input_1>
        Surname <user_input_2>
        Age <user_input_3>

    Args:
        list_labels (list): labels of inputs
        title (string): title of the "input section"

    Returns:
        list: List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """
    if title != "":
        print(f'\n{title}')
    inputs = []
    for label in list_labels:
        while True:
            user_input = input(label).strip()
            if label in ["Please enter a number: ", "ID: "]:
                break
            else:
                try:
                    user_input = common.get_input_valid(user_input, label)
                except ValueError as err:
                    print_error_message("Incorrect input. " + str(err))
                else:
                    break
        inputs.append(user_input)
    return inputs


def print_error_message(message):
    """
    Displays an error message (example: ``Error: @message``)

    Args:
        message (str): error message to be displayed

    Returns:
        None: This function doesn't return anything it only prints to console.
    """
    print(f'Error: {message}')
