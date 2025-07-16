from colorama import Fore, init
from bot_config import bot_config
from bot_utils import utils
from commands import command_handlers


init(autoreset=True)


def main():
    print(f"{Fore.GREEN} Bot is starting...")
    print(f"{Fore.BLUE} Welcome to the Bot Assistant!")
    book = utils.load_data()

    while True:
        command = utils.get_user_input("Enter a command (or 'exit' to quit): ")

        if command in bot_config.exit.command:
            print(f"{Fore.GREEN}{bot_config.exit.answer}")
            utils.save_data(book)
            break

        elif command in bot_config.greeting.command:
            print(f"{Fore.GREEN}{bot_config.greeting.answer}")

        elif command in command_handlers:
            command_handlers[command](book)

        else:
            print(f"{Fore.RED} {bot_config.unknown_command.answer}")


if __name__ == "__main__":
    main()
