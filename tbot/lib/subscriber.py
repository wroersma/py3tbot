import random


def get_subscribers_file():
    """"""
    print("nothing")


def get_sub_list(subscribers_file) -> list:
    """get_subscribers_file"""
    with open(subscribers_file, 'r') as sub_file:
        sub_list = sub_file.readlines()
        return sub_list


def return_random_sub_name(sub_list) -> str:
    number_of_subs = len(sub_list)
    number_of_subs -= 1
    select_winner = random.randint(1, int(number_of_subs))
    name = sub_list[select_winner]
    return str(name[26:-1])


