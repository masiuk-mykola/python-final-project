from box import Box
from colorama import Fore, init

init(autoreset=True)

greeting_commands = ["hello", "hi", "hey"]
exit_bot_commands = ["exit", "close", "q"]

bot_config = Box(
    {
        "greeting": {
            "command": greeting_commands,
            "answer": "Hello! How can I help you?",
        },
        "exit": {"command": exit_bot_commands, "answer": "Goodbye! Have a great day!"},
        "unknown_command": {
            "answer": "Invalid command.",
        },
        "add": {"command": "add", "answer": "Contact added."},
        "change": {
            "command": "change",
            "answer": {
                "success": "Contact updated.",
                "fail": "Contact not found.",
            },
        },
        "phone": {
            "command": "phone",
            "answer": {
                "success": lambda contact: f"{contact}",
                "fail": lambda name: f"{name} not found in contacts.",
            },
        },
        "all": {"command": "all"},
        "delete": {
            "command": "delete",
            "answer": {
                "success": lambda name: f"Contact {name} deleted successfully.",
                "fail": lambda name: f"Contact {name} not found.",
            },
        },
        "remove_phone": {
            "command": "remove-phone",
            "answer": {
                "success": lambda name, phone: f"Phone {phone} removed from {name}.",
                "fail": lambda name, phone: f"Phone {phone} not found for {name}.",
            },
        },
        "add_birthday": {"command": "add-birthday", "answer": "Birthday added."},
        "show_birthday": {"command": "show-birthday", "answer": "Birthday shown."},
        "birthdays": {"command": "birthdays", "answer": "Upcoming birthdays shown."},
        "search": {"command": "search"},
        "add_note": {
            "command": "add-note",
            "answer": "Note added.",
        },
        "search_note": {
            "command": "search-note",
            "answer": "Search results:",
        },
        "edit_note": {
            "command": "edit-note",
            "answer": {
                "success": "Note edited.",
                "fail": "Note not found.",
            },
        },
        "delete_note": {
            "command": "delete-note",
            "answer": {
                "success": "Note deleted.",
                "fail": "Note not found.",
            },
        },
        "sort_notes_by_tag": {
            "command": "sort-notes",
            "answer": "Notes sorted by tag.",
        },
        "add_email": {
            "command": "add-email",
            "answer": {
                "success": "Email added successfully.",
                "fail": "Invalid email format.",
            },
        },
        "edit_email": {
            "command": "edit-email",
            "answer": {
                "success": "Email updated successfully.",
                "fail": "Invalid email format or contact not found.",
            },
        },
        "remove_email": {
            "command": "remove-email",
            "answer": "Email removed.",
        },
        "list_notes": {
            "command": "notes-list",
            "answer": "Here are all your notes:",
        },
    }
)