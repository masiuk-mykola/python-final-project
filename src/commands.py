from bot_config import bot_config
from bot_utils import utils


command_handlers = {
    bot_config.add.command: utils.add,
    bot_config.change.command: utils.change,
    bot_config.phone.command: utils.phone,
    bot_config.all.command: utils.all,
    bot_config.delete.command: utils.delete,
    bot_config.remove_phone.command: utils.remove_phone,
    bot_config.add_birthday.command: utils.add_birthday,
    bot_config.show_birthday.command: utils.show_birthday,
    bot_config.birthdays.command: utils.show_upcoming_birthdays,
    bot_config.search.command: utils.search,
}
