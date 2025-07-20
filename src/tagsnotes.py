from collections import defaultdict

class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __repr__(self):
        return f"Note(text={self.text!r}, tags={self.tags!r})"

class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.notes.append(note)

    def find_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    def sort_by_tag(self):
        return sorted(self.notes, key=lambda note: note.tags)

    def get_all_notes(self):
        return self.notes
