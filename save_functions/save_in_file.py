from text_ui import get_choice
import csv
import os


def create_new_file(filename, first_row):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(first_row)


def add_to_file(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(data)


def save_in_csv_question(data, filename):
    print("Do you want to save in csv file? (input: y/n)")
    choice = get_choice.get_user_input()
    match choice:
        case 'y':
            if os.path.isfile(filename):
                add_to_file(filename, data)
            else:
                if len(data[0]) == 3:
                    create_new_file(filename, first_row=['protonmail address', 'protonmail password', 'date and time'])
                else:
                    create_new_file(filename, first_row=['protonmail address',
                                                         'protonmail password', 'jetbrains password', 'date and time'])
                add_to_file(filename, data)
            print('saved')
        case 'n':
            pass
