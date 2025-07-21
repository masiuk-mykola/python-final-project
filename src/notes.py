class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        return f"Note(text='{self.text}', tags={self.tags})"


class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def search_notes(self, keyword=None, tag=None):
        result = []
        for note in self.notes:
            if keyword and keyword.lower() in note.text.lower():
                result.append(note)
            elif tag and tag.lower() in [t.lower() for t in note.tags]:
                result.append(note)
        return result

    def edit_note(self, index, new_text=None, new_tags=None):
        if 0 <= index < len(self.notes):
            if new_text:
                self.notes[index].text = new_text
            if new_tags is not None:
                self.notes[index].tags = new_tags

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            self.notes.pop(index)

    def sort_by_tag(self):
        return sorted(self.notes, key=lambda note: note.tags)