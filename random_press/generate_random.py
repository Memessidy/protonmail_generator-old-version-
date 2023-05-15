from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import random


def generate_password(min_length, max_length, use_special_symbols=False, use_digits=False, custom_symbols=None):
    length = random.randint(min_length, max_length)
    if use_special_symbols and use_digits:
        possible_chars = ascii_uppercase + ascii_lowercase + digits + punctuation
    elif use_digits:
        possible_chars = ascii_uppercase + ascii_lowercase + digits
    elif use_special_symbols:
        possible_chars = ascii_uppercase + ascii_lowercase + punctuation
    else:
        possible_chars = ascii_uppercase + ascii_lowercase

    first_char = random.choice(ascii_lowercase)
    length -= 1

    random_string = ''
    for _ in range(length):
        random_string += random.choice(possible_chars)
    random_string = first_char + random_string

    if custom_symbols:
        random_list = list(random_string)
        index = random.randint(2, min_length-6)
        for symbol in custom_symbols:
            random_list.insert(index, symbol)
            index += random.randint(2, 5)
        random_string = ''.join(random_list)
    return random_string


# print(generate_password(15, 20, custom_symbols=['-', '_']))
