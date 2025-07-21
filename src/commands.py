from bot_config import bot_config
from bot_utils import utils
from note_commands import add_note, search_note, edit_note, delete_note, sort_notes_by_tag
from note_commands import list_notes


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
    bot_config.add_note.command: add_note,
    bot_config.search_note.command: search_note,
    bot_config.edit_note.command: edit_note,
    bot_config.delete_note.command: delete_note,
    bot_config.list_notes.command: list_notes,
    bot_config.sort_notes_by_tag.command: sort_notes_by_tag,
    bot_config.add_email.command: utils.add_email,
    bot_config.edit_email.command: utils.edit_email,
    bot_config.remove_email.command: utils.remove_email,
}
