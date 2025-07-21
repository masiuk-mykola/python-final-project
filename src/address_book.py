from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """
    Base class for storing field values.

    Attributes:
    value: Field value (of any type).
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    A class to represent a contact name.

    Checks that the name is a string and not empty.
    """

    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name is required and must be a string")
        super().__init__(value)


class Phone(Field):
    """
    A class to represent a phone.

    Stores the value as a string.
    """

    def __init__(self, value):
        super().__init__(str(value))


class Birthday(Field):
    """
    A class for representing a date of birth.

    Accepts a date in the format DD.MM.YYYY.
    """

    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """
    Represents a single entry (contact) in the address book.

    Attributes:
    name (Name): The name of the contact.
    phones (list): List of phones.
    birthday (Birthday | None): Date of birth (optional).
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_name(self, old_name, new_name, book):
        if self.name.value == old_name:
            book.data.pop(old_name)
            self.name = Name(new_name)
            book.data[new_name] = self
            print(f"Name changed from {old_name} to {new_name}")
        else:
            print(f"Error: current name does not match {old_name}")

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, query):
        return [p for p in self.phones if query in p.value]

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else '-'}"

    def add_email(self, email):
        self.email = email

    def edit_email(self, new_email):
        self.email = new_email

    def remove_email(self):
        self.email = None

    def __str__(self):
        result = f"Name: {self.name}, Phones: {[p.value for p in self.phones]}"
        if self.birthday:
            result += f", Birthday: {self.birthday.value}"
        if self.email:
            result += f", Email: {self.email}"
        return result


class AddressBook(UserDict):
    """
    The AddressBook class is designed to store and manage user contacts.

    Contacts can contain multiple phone numbers, birth dates, and notes.
    The functions add, modify, search, and delete contacts and notes are supported.

    Attributes:
    contacts (dict): A dictionary with contact records, where the key is a name, the value is a contact object.

    Methods:
    add_record(): Adds a new contact.
    search(): Search for a contact by name or phone.
    delete_record(): Deletes a contact.
    """

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        return self.data.pop(name, None)

    def get_upcoming_birthdays(self, days_ahead=7):
        today = datetime.today().date()
        upcoming_birthdays = []

        for contact in self.data.values():
            if not contact.birthday:
                continue

            birthday = contact.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days

            if 0 <= delta_days <= days_ahead:
                upcoming_birthdays.append(contact)

        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "AddressBook is empty"
        return "\n".join(str(record) for record in self.data.values())
