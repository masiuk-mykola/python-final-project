import re
from box import Box
from colorama import Fore, init
import pickle
from prompt_toolkit import prompt

from address_book import AddressBook, Record
from bot_autocomplete import DynamicCompleter
from bot_config import bot_config
from constants import patterns

init(autoreset=True)


def validator(pattern, string_to_validate):
    match = re.search(re.compile(pattern), string_to_validate)
    if match:
        return True
    else:
        return False


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
def add_contact(book):
    name = get_user_input("Enter contact name: ")
    phone = get_user_input("Enter contact phone: ")

    record = book.find(name)

    if record is None:
        if validator(patterns.phone, phone):
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"{Fore.GREEN} Додано новий контакт {name}: {phone}")
        else:
            print("Error: Некоректний номер, контакт не створено.")
    else:
        if validator(patterns.phone, phone):
            if phone in [p.value for p in record.phones]:
                print(f"{Fore.YELLOW} Номер {phone} вже існує для {name}")
            else:
                record.add_phone(phone)
                print(f"{Fore.GREEN} Додано номер до {name}: {phone}")
        else:
            print("Error: Некоректний номер.")


def edit_contact_field(book, name, field_type):
    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} {bot_config.change.answer.fail}")
        return

    if field_type == "name":
        new_name = get_user_input("Enter new contact name: ")
        try:
            contact.edit_name(name, new_name, book)
            print(f"{Fore.GREEN} {bot_config.change.answer.success}")
        except ValueError as e:
            print(f"{Fore.RED} Failed to change name: {e}")

    elif field_type == "phone":
        old_phone = get_user_input("Enter contact phone to change: ")
        new_phone = get_user_input("Enter new contact phone: ")
        try:
            contact.edit_phone(old_phone, new_phone)
            print(f"{Fore.GREEN} {bot_config.change.answer.success}")
        except ValueError as e:
            print(f"{Fore.RED} Failed to change phone: {e}")


@input_error
def change_contact(book):
    name = get_user_input("Enter contact name to change: ")

    print("Choose the option you want to change:\n1 - name\n2 - phone")
    cmd = get_user_input("Your choice: ")

    if cmd == "1":
        edit_contact_field(book, name, "name")
    elif cmd == "2":
        edit_contact_field(book, name, "phone")
    else:
        print(f"{Fore.RED} {bot_config.unknown_command.answer}")


@input_error
def show_phone(book):
    name = get_user_input("Enter contact name to show phone: ")

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


def delete_contact(book):
    name = get_user_input("Enter contact name to delete: ")

    if book.delete(name):
        print(f"{Fore.GREEN} Contact {name} deleted successfully.")
    else:
        print(f"{Fore.RED} Contact {name} not found.")


def remove_phone(book):
    name = get_user_input("Enter contact name: ")
    phone = get_user_input("Enter contact phone to remove: ")

    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} {bot_config.phone.answer.fail(name)}")
        return

    if contact.remove_phone(phone):
        print(f"{Fore.GREEN} Phone {phone} removed from {name}.")
    else:
        print(f"{Fore.RED} Phone {phone} not found for {name}.")


def add_birthday(book):
    name = get_user_input("Enter contact name: ")
    birthday = get_user_input("Enter contact birthday: ")

    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} Contact {name} not found.")
        return

    try:
        contact.add_birthday(birthday)
        print(f"{Fore.GREEN} Birthday for {name} added successfully.")
    except ValueError as e:
        print(f"{Fore.RED} Failed to add birthday: {e}")


def show_birthday(book):
    name = get_user_input("Enter contact name: ")

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


def search(book):
    name = get_user_input("Enter contact name to change: ")
    contact = book.find(name)
    print(contact)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def save_commands(command, filename="commands.pkl"):
    try:
        with open(filename, "rb") as f:
            commands = pickle.load(f)
    except FileNotFoundError:
        commands = []

    if command not in commands:
        commands.append(command)

    with open(filename, "wb") as f:
        pickle.dump(commands, f)


def load_commands(filename="commands.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return extract_commands(bot_config)


def extract_commands(config):
    commands = []
    for item in config.values():
        command = item.get("command")
        if isinstance(command, list):
            commands.extend(command)
        elif isinstance(command, str):
            commands.append(command)
    return commands


predefined_commands = extract_commands(bot_config)
history_commands = load_commands()

all_commands = list(set(predefined_commands + history_commands))


def get_user_input(message):
    cmd = prompt(message, completer=DynamicCompleter(all_commands)).strip()
    save_commands(cmd)
    return cmd


utils = Box(
    {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "delete": delete_contact,
        "remove_phone": remove_phone,
        "add_birthday": add_birthday,
        "show_birthday": show_birthday,
        "show_upcoming_birthdays": show_upcoming_birthdays,
        "load_data": load_data,
        "save_data": save_data,
        "search": search,
        "save_commands": save_commands,
        "load_commands": load_commands,
        "extract_commands": extract_commands,
        "get_user_input": get_user_input,
    }
)
