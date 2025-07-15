from box import Box
from colorama import Fore, init
import pickle

from address_book import AddressBook, Record
from bot_config import bot_config

init(autoreset=True)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print(f"{Fore.RED} Error: {bot_config.phone.answer.fail(args[0][0])}.")
        except ValueError:
            print(f"{Fore.RED} Error: Enter the argument for the command")
        except IndexError:
            print(f"{Fore.RED} Error: Enter user name.")
        except TypeError:
            print(f"{Fore.RED} Error: Invalid command or missing data.")

    return inner


def check_args_length(
    args,
    expected_length=2,
):
    if len(args) < expected_length:
        raise ValueError("Insufficient arguments")
    return True


@input_error
def add_contact(args, book):
    check_args_length(args)

    name, phone = args[0], args[1]
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    if phone:
        record.add_phone(phone)

    print(f"{Fore.GREEN} {bot_config.add.answer} {name}: {phone}")


@input_error
def change_contact(args, book):
    check_args_length(args, 3)

    name, old_phone, new_phone = args[0], args[1], args[2]
    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} {bot_config.change.answer.fail}")
        return

    try:
        contact.edit_phone(old_phone, new_phone)
        print(f"{Fore.GREEN} {bot_config.change.answer.success}")
    except ValueError as e:
        print(f"{Fore.RED} Failed to change phone: {e}")


@input_error
def show_phone(args, book):
    check_args_length(args, 1)

    name = args[0]
    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} {bot_config.phone.answer.fail(name)}")
        return

    else:
        print(f"{Fore.GREEN} {bot_config.phone.answer.success(contact)}")


@input_error
def show_all(book):
    if not book:
        print(f"{Fore.YELLOW} No contacts found.")
        print(book.data)
    for _, record in book.data.items():
        print(f"{Fore.GREEN} {record}")


def delete_contact(args, book):
    check_args_length(args, 1)

    name = args[0]
    if book.delete(name):
        print(f"{Fore.GREEN} Contact {name} deleted successfully.")
    else:
        print(f"{Fore.RED} Contact {name} not found.")


def remove_phone(args, book):
    check_args_length(args, 2)

    name, phone = args[0], args[1]
    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} {bot_config.phone.answer.fail(name)}")
        return

    if contact.remove_phone(phone):
        print(f"{Fore.GREEN} Phone {phone} removed from {name}.")
    else:
        print(f"{Fore.RED} Phone {phone} not found for {name}.")


def add_birthday(args, book):
    check_args_length(args, 2)

    name, birthday = args[0], args[1]
    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} Contact {name} not found.")
        return

    try:
        contact.add_birthday(birthday)
        print(f"{Fore.GREEN} Birthday for {name} added successfully.")
    except ValueError as e:
        print(f"{Fore.RED} Failed to add birthday: {e}")


def show_birthday(args, book):
    check_args_length(args, 1)

    name = args[0]
    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} Contact {name} not found.")
        return

    if contact.birthday:
        print(f"{Fore.GREEN} Birthday for {name}: {contact.birthday.value}")
    else:
        print(f"{Fore.YELLOW} No birthday set for {name}.")


def show_upcoming_birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        print(f"{Fore.YELLOW} No upcoming birthdays found.")
        return

    print(f"{Fore.GREEN} Upcoming birthdays:")
    for contact in upcoming_birthdays:
        print(contact)
        print(f"{contact['name']}: {contact['congratulation_date']}")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


utils = Box(
    {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "parse_input": parse_input,
        "delete": delete_contact,
        "remove_phone": remove_phone,
        "add_birthday": add_birthday,
        "show_birthday": show_birthday,
        "show_upcoming_birthdays": show_upcoming_birthdays,
        "load_data": load_data,
        "save_data": save_data,
    }
)
