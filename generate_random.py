import random
import string


def generate_password(min_length, max_length, use_digits=False):
    length = random.randint(min_length, max_length)
    """Generates a random password of the specified length."""
    chars = string.ascii_letters + string.digits if use_digits else string.ascii_letters
    one_char = random.choice('abcdefghkljiuqwx')
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return one_char + password

