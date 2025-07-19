import re
from colorama import Fore, init
from box import Box

init(autoreset=True)


def validator(pattern, string_to_validate):
    match = re.search(re.compile(pattern), string_to_validate)
    if match:
        return True
    else:
        return False


logger = Box(
    {
        "log": lambda message: print(f"{message}"),
        "success": lambda message: print(f"✅{Fore.GREEN}{message}"),
        "warn": lambda message: print(f"⚠️{Fore.YELLOW}{message}"),
        "error": lambda message: print(f"‼️{Fore.RED}{message}"),
    }
)
