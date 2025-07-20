from notes import NotesManager

def main():
    manager = NotesManager()

    # Додавання нотаток
    manager.add_note("Купити молоко", ["покупки", "домашнє"])
    manager.add_note("Вивчити Python", ["навчання", "програмування"])
    manager.add_note("Зустріч з другом", ["зустріч", "особисте"])

    print("\nУсі нотатки:")
    for note in manager.get_all_notes():
        print(note)

    print("\nНотатки з тегом 'програмування':")
    for note in manager.find_by_tag("програмування"):
        print(note)

    print("\nНотатки, відсортовані за тегами:")
    for note in manager.sort_by_tag():
        print(note)

if __name__ == "__main__":
    main()
