import random

from email_services.email_interface import MailBox
import settings
from random_press.generate_random import generate_password, get_username
from faker import Faker


class Unit:
    def __init__(self):
        self.__user_name = None
        self.__mail_box = None
        self.__password = None
        self.domains = {
            'guerrilla': '@guerrillamail.com',
            'maildrop': '@maildrop.cc',
            'dropjar': '@dropjar.com',
            'inboxbear': '@inboxbear.com',
            'tafmail': '@tafmail.com'
        }
        self.__first_name = None
        self.__last_name = None
        self.generate_values()

    @property
    def mail_box(self):
        return self.__mail_box

    @mail_box.setter
    def mail_box(self, value: MailBox):
        if not isinstance(value, MailBox):
            raise ValueError('Mail box must be a mail box')
        self.__mail_box = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value < 10):
            raise ValueError('Password is too short')
        self.__password = value

    @property
    def user_name(self):
        return self.__user_name

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    def generate_values(self):
        fake = Faker()
        self.__user_name = get_username()
        try:
            self.__mail_box = MailBox()
            self.__mail_box.box_name = self.user_name.replace('-', '').replace('_', '')
            self.__mail_box.domain = self.domains[settings.temporary_email]
        except Exception as exc:
            raise ValueError('Check your temporary email in settings')
        # use_special_symbols = random.choice([True, False])
        use_digits = random.choice([True, False])
        self.__password = generate_password(min_length=25, max_length=35, use_digits=use_digits,
                                            use_special_symbols=False)
        self.__first_name = fake.first_name()
        self.__last_name = fake.last_name()

    def get_person(self):
        result = {
            'first_name': self.first_name,
            'last name': self.last_name,
            'password': self.password}
        return result
