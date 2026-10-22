"""Точка входа в приложение эмулятора."""
import argparse
from shell import Shell


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", help="Путь к VFS")
    parser.add_argument("--script", help="Путь к скрипту")
    return parser.parse_args()


def run_script(script_path, shell):
    """
    Выполняет команды из стартового скрипта.

    Поддерживает комментарии и эхо-вывод.
    """
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                print(f"{shell.vfs_name}> {line}")
                shell.execute(line)
    except FileNotFoundError:
        print(f"Ошибка: скрипт '{script_path}' не найден.")
    except Exception as e:
        print(f"Ошибка при выполнении скрипта: {e}")


def main():
    """Точка входа в приложение."""
    args = parse_args()

    print("Параметры запуска:")
    print(f"  VFS путь: {args.vfs or 'не задан'}")
    print(f"  Скрипт: {args.script or 'не задан'}")

    shell = Shell()

    if args.script:
        run_script(args.script, shell)
    else:
        shell.run_repl()


if __name__ == "__main__":
    main()