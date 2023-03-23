import random
import string


def generate_password(min_length, max_length, use_digits=False):
    length = random.randint(min_length, max_length)
    """Generates a random password of the specified length."""
    char_1 = random.choice(string.ascii_letters)
    chars = string.ascii_letters + string.digits if use_digits else string.ascii_letters
    password = ''
    for i in range(length-1):
        password += random.choice(chars)
    return char_1 + password
