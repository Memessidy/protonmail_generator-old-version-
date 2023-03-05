import csv
from generator import new_protonmail


class MyGenerator:
    def __init__(self):
        self.__bad_tries_counter = 0
        # В коротких періодах - 5, в довгих 15 (3*5)
        self.sleeping_time = 5
        # Кількість невдалих спроб, після досягнення стоп
        self.stop_on_bad_tries = 2
        # Кількість спроб всього
        self.num_of_tries = 1
        self.filename = "data.csv"
        self.use_capcha = False
        self.data = None
        self.temporary_mail = "maildrop"

    def run_generator(self):
        for i in range(self.num_of_tries):
            if self.__bad_tries_counter >= self.stop_on_bad_tries:
                print("Number of bad tries reached. Stopping...")
                return
            try:
                self.__bad_tries_counter += self.get_email()
            except Exception as exc:
                print("One error has been excepted:")
                print(exc)
                continue

    def get_email(self):
        self.data = new_protonmail(self.use_capcha, self.sleeping_time, self.temporary_mail)
        if self.data is None:
            print("Bad try! Stopping current...")
            return 1
        return 0

    def write_data(self):
        with open(self.filename, mode='a', encoding='utf-8', newline='') as f:
            fieldnames = ['login', 'password']
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writerow(self.data)


if __name__ == '__main__':
    print("Starting...")
    gen = MyGenerator()
    gen.run_generator()
    print("Writing...")
    gen.write_data()
    # print(gen.data)
    input("Type something to exit;")