def get_valid_input(user_input, label):
    """
    Args:
        input type list: what kind of input data valaidation needed

    Returns:
        string: Random and unique string
    """
    message_incorrect = "Incorrect input."

    if label == "Month: ":
        if int(user_input) in range(1, 13):
            return user_input
        else:
            raise ValueError

    if label == "Day: ":
        if int(user_input) in range(1, 32):
            return user_input
        else:
            raise ValueError

    if label in ["Purchase Year: ", "Year: "]:
        if int(user_input) in range(2000, 2020):
            return user_input
        else:
            raise ValueError

    if label == "Type: ":
        user_input = user_input.lower()
        if user_input in ["in", "out"]:
            return user_input
        else:
            raise ValueError

    if label == "Amount: ":
        if int(user_input) in range(1-2001):
            return user_input
        else:
            raise ValueError

    if label == "Name: ":
        name_parts = [name_part.title() for name_part in user_input.split(" ")]
        if len(name_parts) > 1 and all(len(name_part) > 2 for name_part in name_parts):
            return " ".join(name_parts)
        else:
            raise ValueError

    if label == "E-mail: ":
        if user_input.count("@") == 1 and user_input.count(".") > 0:
            return user_input.lower()
        else:
            raise ValueError

    if label == "Subscripted: ":
        if int(user_input) in [1, 0]:
            return user_input
        else:
            raise ValueError

    if label == "Birth Year: ":
        if int(user_input) in range(1920, 2002):
            return user_input
        else:
            raise ValueError

    if label == "Manufacturer":
        if len(user_input) > 2:
            return user_input
        else:
            raise ValueError

    if label == "Durability: ":
        if int(user_input) in range(1, 11):
            return user_input
        else:
            raise ValueError

    if label == "Title: ":
        if len(user_input) > 2:
            return user_input
        else:
            raise ValueError

    if label == "Price: ":
        if int(user_input) in range(1, 201):
            return user_input
        else:
            raise ValueError

    elif label == "In Stock: ":
        if int(user_input) >= 0:
            return user_input
        else:
            raise ValueError

    else:
        return user_input





def get_valid_input(user_input, label):
    """
    Args:
        input type list: what kind of input data valaidation needed

    Returns:
        string: Random and unique string
    """
    if label == "Type: ":
        user_input = user_input.lower()
    if label == "Name: ":
        name_parts = [name_part.title() for name_part in user_input.split(" ")]
    CONDITIONS = 0
    RETURN_VALUE = 1
    labels_what_to_do = {
        "Month: ": [int(user_input) in range(1, 13), user_input],
        "Day: ": [int(user_input) in range(1, 32), user_input],
        "Purchase Year: ": [int(user_input) in range(2000, 2020), user_input],
        "Year: ": [int(user_input) in range(2000, 2020), user_input],
        "Type: ": [user_input in ["in", "out"], user_input],
        "Amount: ": [int(user_input) in range(1, 2001), user_input],
        "Name: ": [len(name_parts) > 1 and all(len(name_part) > 2 for name_part in name_parts), " ".join(name_parts)],
        "E-mail: ": [user_input.count("@") == 1 and user_input.count(".") > 0, user_input.lower()],
        "Subscripted: ": [int(user_input) in [1, 0], user_input],
        "Birth Year: ": [int(user_input) in range(1920, 2002), user_input],
        "Manufacturer": [len(user_input) > 2, user_input],
        "Durability: ": [int(user_input) in range(1, 11), user_input],
        "Title: ": [len(user_input) > 2, user_input],
        "Price: ": [int(user_input) in range(1, 201), user_input],
        "In Stock: ": [int(user_input) >= 0, user_input]
    }

    if label not in labels_what_to_do:
        return user_input

    for input_type, handling in labels_what_to_do.items():
        if input_type == label:
            if handling[CONDITIONS]:
                return handling[RETURN_VALUE]
            else:
                raise ValueError