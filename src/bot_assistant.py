from colorama import Fore, init
from address_book import AddressBook
from bot_config import bot_config
from bot_utils import utils

init(autoreset=True)


def main():
    print(f"{Fore.GREEN} Bot is starting...")
    print(f"{Fore.BLUE} Welcome to the Bot Assistant!")
    book = utils.load_data()

    while True:
        user_input = input("Enter a command (or 'exit' to quit): ").strip().lower()
        command, *args = utils.parse_input(user_input)

        if command in bot_config.exit.command:
            print(f"{Fore.GREEN}{bot_config.exit.answer}")
            utils.save_data(book)
            break

        elif command in bot_config.greeting.command:
            print(f"{Fore.GREEN}{bot_config.greeting.answer}")

        elif command == bot_config.add.command:
            utils.add(args, book)

        elif command == bot_config.change.command:
            utils.change(args, book)

        elif command == bot_config.phone.command:
            utils.phone(args, book)

        elif command == bot_config.all.command:
            utils.all(book)

        elif command == bot_config.delete.command:
            utils.delete(args, book)

        elif command == bot_config.remove_phone.command:
            utils.remove_phone(args, book)

        elif command == bot_config.add_birthday.command:
            utils.add_birthday(args, book)

        elif command == bot_config.show_birthday.command:
            utils.show_birthday(args, book)

        elif command == bot_config.birthdays.command:
            utils.show_upcoming_birthdays(book)

        else:
            print(f"{Fore.RED} {bot_config.unknown_command.answer}")


if __name__ == "__main__":
    main()
