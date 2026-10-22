"""Модуль оболочки эмулятора."""
from cmd_parser import parse_command


class Shell:
    """Основной класс эмулятора оболочки."""

    def __init__(self, vfs_name="MyVFS"):
        """Инициализация оболочки с именем VFS."""
        self.vfs_name = vfs_name
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }
        self.is_running = True

    def cmd_ls(self, args):
        """Заглушка команды ls."""
        print(f"Команда: ls, аргументы: {args}")

    def cmd_cd(self, args):
        """Заглушка команды cd."""
        print(f"Команда: cd, аргументы: {args}")

    def cmd_exit(self, args):
        """Команда выхода из эмулятора."""
        print("Выход из эмулятора.")
        self.is_running = False

    def execute(self, input_str):
        """Выполняет одну строку ввода."""
        args = parse_command(input_str)
        if not args:
            return

        cmd_name = args[0]
        cmd_args = args[1:]

        if cmd_name in self.commands:
            self.commands[cmd_name](cmd_args)
        else:
            print(f"Ошибка: неизвестная команда '{cmd_name}'")

    def run_repl(self):
        """Запуск интерактивного режима (REPL)."""
        print(f"Эмулятор запущен. VFS: {self.vfs_name}")
        while self.is_running:
            try:
                user_input = input(f"{self.vfs_name}> ")
                self.execute(user_input)
            except EOFError:
                break