from notes import Note, NoteBook
from colorama import Fore
from bot_config import bot_config
from storage import save_data, load_data

FILENAME = "notebook.pkl"
note_book = load_data(FILENAME)
if note_book is None:
    note_book = NoteBook()

def add_note(book=None):
    text = input("Enter note text: ")
    tags_input = input("Enter tags (comma-separated, optional): ")
    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []

    note = Note(text, tags)
    note_book.add_note(note)
    save_data(note_book, FILENAME)
    print(f"{Fore.GREEN} {bot_config.add_note.answer}")

def search_note(book=None):
    search_type = input("Search by [1] keyword or [2] tag? ")
    if search_type == "1":
        keyword = input("Enter keyword: ")
        results = note_book.search_notes(keyword=keyword)
    elif search_type == "2":
        tag = input("Enter tag: ")
        results = note_book.search_notes(tag=tag)
    else:
        print("Invalid choice.")
        return

    if results:
        print(f"{Fore.GREEN} {bot_config.search_note.answer}")
        for idx, note in enumerate(results, 1):
            print(f"{idx}. {note}")
    else:
        print(f"{Fore.YELLOW} No matching notes found.")

def edit_note(book=None):
    if not note_book.notes:
        print(f"{Fore.YELLOW} No notes to edit.")
        return

    for idx, note in enumerate(note_book.notes, 1):
        print(f"{idx}. {note}")

    try:
        index = int(input("Enter note number to edit: ")) - 1
        new_text = input("New text (leave empty to keep current): ")
        tags_input = input("New tags (comma-separated, leave empty to keep current): ")
        new_tags = [t.strip() for t in tags_input.split(",")] if tags_input else None

        note_book.edit_note(index, new_text or None, new_tags)
        save_data(note_book, FILENAME)
        print(f"{Fore.GREEN} {bot_config.edit_note.answer.success}")
    except (ValueError, IndexError):
        print(f"{Fore.RED} {bot_config.edit_note.answer.fail}")

def delete_note(book=None):
    if not note_book.notes:
        print(f"{Fore.YELLOW} No notes to delete.")
        return

    for idx, note in enumerate(note_book.notes, 1):
        print(f"{idx}. {note}")

    try:
        index = int(input("Enter note number to delete: ")) - 1
        note_book.delete_note(index)
        save_data(note_book, FILENAME)
        print(f"{Fore.GREEN} {bot_config.delete_note.answer.success}")
    except (ValueError, IndexError):
        print(f"{Fore.RED} {bot_config.delete_note.answer.fail}")

def sort_notes_by_tag(book=None):
    sorted_notes = note_book.sort_by_tag()
    if sorted_notes:
        print(f"{Fore.GREEN} {bot_config.sort_notes_by_tag.answer}")
        for idx, note in enumerate(sorted_notes, 1):
            print(f"{idx}. {note}")
    else:
        print(f"{Fore.YELLOW} No notes available.")