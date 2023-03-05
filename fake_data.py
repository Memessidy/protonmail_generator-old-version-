from faker import Faker
fake = Faker()


def get_person():
    first_name = fake.first_name()
    last_name = fake.last_name()
    password_length = fake.random_int(min=11, max=31)
    password = fake.password(length=password_length, special_chars=False)
    text = fake.text()
    nickname = first_name + text.replace(' ', '')[:11].lower() + last_name
    email = fake.email()
    email_nick = (first_name + email.split('@')[0]).lower()
    return {'first name': first_name, 'last name': last_name,
            'nickname': nickname, 'password': password,
            'email nickname': email_nick}


if __name__ == '__main__':
    person = get_person()
    print(person)

