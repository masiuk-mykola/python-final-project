from bot_utils import utils

command_handlers = {
    "add": utils.add,
    "change": utils.change,
    "phone": utils.phone,
    "all": utils.all,
    "delete": utils.delete,
    "remove-phone": utils.remove_phone,
    "add-birthday": utils.add_birthday,
    "show-birthday": utils.show_birthday,
    "birthdays": utils.show_upcoming_birthdays,
    "search": utils.search,
}
