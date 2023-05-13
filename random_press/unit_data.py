from email_services.email_interface import MailBox
import settings
from random_press.generate_random import generate_password
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
        try:
            self.__mail_box = MailBox()
            self.__mail_box.box_name = generate_password(min_length=9, max_length=12, use_digits=False)
            self.__mail_box.domain = self.domains[settings.temporary_email]
        except Exception as exc:
            raise ValueError('Check your temporary email in settings')
        self.__password = generate_password(min_length=18, max_length=30, use_digits=True)
        # self.__user_name = generate_password(min_length=10, max_length=18, use_digits=False)
        self.__first_name = fake.first_name()
        self.__last_name = fake.last_name()
        self.__user_name = (generate_password(min_length=2, max_length=5, use_digits=False) + self.__first_name +\
            generate_password(min_length=2, max_length=3, use_digits=True) + self.__last_name +\
                           "-" + generate_password(min_length=3, max_length=6, use_digits=True)).capitalize()

    def get_person(self):
        result = {
            'first_name': self.first_name,
            'last name': self.last_name,
            'password': self.password}
        return result
