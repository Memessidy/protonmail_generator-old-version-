import csv
from generator import new_protonmail
import settings


class MyGenerator:
    def __init__(self, num_of_tries=1):
        self.__bad_tries_counter = 0
        self.max_sleeping_time = settings.max_sleeping_time
        self.min_sleeping_time = settings.min_sleeping_time
        self.sleeping_time_middle = settings.middle_sleeping_time
        # Кількість невдалих спроб, після досягнення стоп
        self.stop_on_bad_tries = settings.stop_on_bad_tries
        # Кількість спроб всього
        self.num_of_tries = num_of_tries
        self.filename = settings.filename
        self.data = None
        # guerrilla or maildrop

    def run_generator(self):
        for i in range(self.num_of_tries):
            if self.__bad_tries_counter >= self.stop_on_bad_tries:
                print("Number of bad tries reached. Stopping...")
                return
            else:
                self.__bad_tries_counter += self.get_email()

    def get_email(self):
        try:
            self.data = new_protonmail(sleeping_time_min=self.min_sleeping_time,
                                       sleeping_time_max=self.max_sleeping_time,
                                       sleeping_time_middle=self.sleeping_time_middle)
            self.write_data()
            print("Writing...")
            return 0
        except Exception as exc:
            print(exc)
            print("Bad try! Stopping current...")
            return 1

    def write_data(self):
        with open(self.filename, mode='a', encoding='utf-8', newline='') as f:
            fieldnames = ['login', 'password']
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writerow(self.data)


def main():
    print("На 1 ip за добу можна згенерувати приблизно 4 адреси")
    num_of_tries = 0
    num_of_tries = input("Введіть бажану кількість адресів: ")
    if not num_of_tries.isdigit():
        print("Повинно бути ціле число!!!")
        return
    else:
        print("Starting...")
        gen = MyGenerator(num_of_tries=int(num_of_tries))
        gen.run_generator()
        input("Type something to exit;")


if __name__ == '__main__':
    main()
