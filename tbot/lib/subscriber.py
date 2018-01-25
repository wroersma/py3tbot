import random


def get_subscribers_file():
    """"""
    # TODO make a subscribers_file get from API function to check for an update every time we run
    print("this is a place holder for a future function")


def get_sub_list(subscribers_file) -> list:
    """get_subscribers_file"""
    with open(subscribers_file, 'r') as sub_file:
        sub_list = sub_file.readlines()
        return sub_list


def get_user_name_list(sub_list) -> list:
    user_list = []
    for item in sub_list:
        user_list.append(item[26:-1])
    user_list.remove('')
    return user_list


def get_non_winning_sub_list(sub_user_name_list, winner_list) -> list:
    non_winning_sub_list = []
    string_user_name_winner_list = []
    for item in winner_list:
        user_name_object = [item][0]
        user_name = (str(user_name_object)[7:-2])
        if item != user_name:
            string_user_name_winner_list.append(user_name)
    for user_name_item in sub_user_name_list:
        if user_name_item not in string_user_name_winner_list:
            non_winning_sub_list.append(user_name_item)
    return non_winning_sub_list


def return_random_sub_name(sub_user_name_list) -> str:
    number_of_subs = len(sub_user_name_list)
    select_winner = random.randint(0, int(number_of_subs))
    name = sub_user_name_list[select_winner]
    return str(name)
