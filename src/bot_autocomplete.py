from prompt_toolkit.completion import Completer, Completion


class DynamicCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        word = document.text_before_cursor
        for command in self.commands:
            if command.startswith(word):
                yield Completion(command, start_position=-len(word))
