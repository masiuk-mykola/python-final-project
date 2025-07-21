from box import Box
import pickle
from prompt_toolkit import prompt
from colorama import Fore, init

init(autoreset=True)

from address_book import AddressBook, Record
from bot_autocomplete import DynamicCompleter
from bot_config import bot_config
from constants import patterns
from utils import validator, logger


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            logger.error(f"Error: {bot_config.phone.answer.fail(args[0][0])}.")
        except ValueError:
            logger.error(f"Error: Enter the argument for the command")
        except IndexError:
            logger.error(f"Error: Enter user name.")
        except TypeError:
            logger.error(f"Error: Invalid command or missing data.")

    return inner


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
            logger.success(f"New contact is added {name}: {phone}")
        else:
            logger.error("Error: Incorrect number, contact not created.")
    else:
        if validator(patterns.phone, phone):
            if phone in [p.value for p in record.phones]:
                logger.warn(f"Phone number {phone} is already exists {name}")
            else:
                record.add_phone(phone)
                logger.success(f"Number added to {name}: {phone}")
        else:
            logger.error("Error: Incorrect number.")


def edit_contact_field(book, name, field_type):
    contact = book.find(name)

    if not contact:
        logger.error(f"{bot_config.change.answer.fail}")
        return

    if field_type == "name":
        new_name = get_user_input("Enter new contact name: ")
        try:
            contact.edit_name(name, new_name, book)
            logger.success(f"{bot_config.change.answer.success}")
        except ValueError as e:
            logger.error(f"Error: Failed to change name: {e}")

    elif field_type == "phone":
        old_phone = get_user_input("Enter contact phone to change: ")
        new_phone = get_user_input("Enter new contact phone: ")
        try:
            contact.edit_phone(old_phone, new_phone)
            logger.success(f"{bot_config.change.answer.success}")
        except ValueError as e:
            logger.error(f"Failed to change phone: {e}")


@input_error
def change_contact(book):
    name = get_user_input("Enter contact name to change: ")

    logger.log("Choose the option you want to change:\n1 - name\n2 - phone")
    cmd = get_user_input("Your choice: ")

    if cmd == "1":
        edit_contact_field(book, name, "name")
    elif cmd == "2":
        edit_contact_field(book, name, "phone")
    else:
        logger.error(f"{bot_config.unknown_command.answer}")


@input_error
def show_phone(book):
    name = get_user_input("Enter contact name to show phone: ")

    contact = book.find(name)

    if not contact:
        logger.error(f"{bot_config.phone.answer.fail(name)}")
        return

    else:
        logger.success(f"{bot_config.phone.answer.success(contact)}")


@input_error
def show_all(book):
    if not book:
        logger.error(f"Error: No contacts found.")
        logger.log(book.data)
    for _, record in book.data.items():
        logger.success(f"{record}")


def delete_contact(book):
    name = get_user_input("Enter contact name to delete: ")

    if book.delete(name):
        logger.success(f"Contact {name} deleted successfully.")
    else:
        logger.error(f"Error: Contact {name} not found.")


def remove_phone(book):
    name = get_user_input("Enter contact name: ")
    phone = get_user_input("Enter contact phone to remove: ")

    contact = book.find(name)

    if not contact:
        logger.error(f"Error: {bot_config.phone.answer.fail(name)}")
        return

    if contact.remove_phone(phone):
        logger.success(f"Phone {phone} removed from {name}.")
    else:
        logger.error(f"Error: Phone {phone} not found for {name}.")


def add_birthday(book):
    name = get_user_input("Enter contact name: ")
    birthday = get_user_input("Enter contact birthday: ")

    contact = book.find(name)

    if not contact:
        logger.error(f"Error: Contact {name} not found.")
        return

    try:
        contact.add_birthday(birthday)
        logger.success(f"Birthday for {name} added successfully.")
    except ValueError as e:
        logger.error(f"Error: Failed to add birthday: {e}")


def show_birthday(book):
    name = get_user_input("Enter contact name: ")

    contact = book.find(name)

    if not contact:
        logger.error(f"Error: Contact {name} not found.")
        return

    if contact.birthday:
        logger.success(f"Birthday for {name}: {contact.birthday.value}")
    else:
        logger.error(f"Error: No birthday set for {name}.")


def show_upcoming_birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    days_ahead = int(get_user_input("Enter days ahead: "))
    upcoming_birthdays = book.get_upcoming_birthdays(days_ahead)

    if not upcoming_birthdays:
        logger.warn(f"No upcoming birthdays found.")
        return

    logger.success(f"Upcoming birthdays:")
    for contact in upcoming_birthdays:
        logger.log(contact)
        logger.log(f"{contact.name}: {contact.birthday}")


def search(book):
    name = get_user_input("Enter contact name to change: ")
    contact = book.find(name)
    logger.log(contact)


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


import re


@input_error
def add_email(book):
    name = get_user_input("Enter contact name: ")
    email = get_user_input("Enter email: ")

    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} Contact {name} not found.")
        return

    if validator(patterns.email, email):
        contact.add_email(email)
        print(f"{Fore.GREEN} {bot_config.add_email.answer.success}")
    else:
        print(f"{Fore.RED} {bot_config.add_email.answer.fail}")


@input_error
def edit_email(book):
    name = get_user_input("Enter contact name: ")
    new_email = get_user_input("Enter new email: ")

    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} Contact {name} not found.")
        return

    if validator(patterns.email, new_email):
        contact.edit_email(new_email)
        print(f"{Fore.GREEN} {bot_config.edit_email.answer.success}")
    else:
        print(f"{Fore.RED} {bot_config.edit_email.answer.fail}")


@input_error
def remove_email(book):
    name = get_user_input("Enter contact name: ")

    contact = book.find(name)

    if not contact:
        print(f"{Fore.RED} Contact {name} not found.")
        return

    contact.remove_email()
    print(f"{Fore.GREEN} {bot_config.remove_email.answer}")


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
        "get_user_input": get_user_input,
        "add_email": add_email,
        "edit_email": edit_email,
        "remove_email": remove_email,
    }
)
