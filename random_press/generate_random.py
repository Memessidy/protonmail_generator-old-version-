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
        for i in custom_symbols:
            random_list.insert(random.randint(1, length-1), i)
        random_string = ''.join(random_list)
    return random_string


# res = generate_password(min_length=10, max_length=14, custom_symbols=['-', '_'], use_digits=True)
# print(res)