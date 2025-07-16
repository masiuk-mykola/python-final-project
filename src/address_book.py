from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):

    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name is required and must be a string")
        super().__init__(value)


class Phone(Field):

    def __init__(self, value):
        super().__init__(str(value))


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        return self.data.pop(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for contact in self.data.values():

            if not contact.name or not contact.birthday:
                return print(
                    "\033[31m‼️ Fields name and birthday are required for each contact.\033[0m"
                )
            else:

                birthday = contact.birthday.value
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days <= 7:
                    if birthday_this_year.weekday() in (5, 6):
                        days_to_monday = 7 - birthday_this_year.weekday()
                        greeting_date = birthday_this_year + timedelta(
                            days=days_to_monday
                        )
                    else:
                        greeting_date = birthday_this_year

                    upcoming_birthdays.append(
                        {
                            "name": contact.name.value,
                            "congratulation_date": greeting_date.isoformat(),
                        }
                    )

        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "AddressBook is empty"
        return "\n".join(str(record) for record in self.data.values())
