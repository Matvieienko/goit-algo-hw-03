from pathlib import Path
from shutil import copyfile
import os

# Введення шляху до вихідної директорії
source = input("Введіть шлях до вихідної директорії: ")
source_folder = Path(source)

# Перевірка існування вихідної папки
if not source_folder.exists() or not source_folder.is_dir():
    print(f"Помилка: Вихідна директорія {source_folder} не існує або не є папкою.")
    exit(1) # Завершення програми через помилку

# Введення шляху до директорії призначення, або встановлення значення за замовчуванням 
output = input("Введіть шлях до директорії призначення (за замовчуванням: 'dist'): ") or (source_folder.parent / "dist")
output_folder = Path(output)

# Перевірка доступу до вихідної папки
if not os.access(source_folder, os.R_OK):
    print(f"Помилка: Немає прав доступу для читання {source_folder}.")
    exit(1)  # Завершення програми через помилку у разі відсутності прав доступу

# Перевірка можливості створення файлів у директорії призначення
if not os.access(output_folder.parent, os.W_OK):
    print(f"Помилка: Немає прав доступу для створення файлів у {output_folder.parent}.")
    exit(1)  

# Функція для рекурсивного читання директорії
# Перебирає всі файли та папки, викликаючи саму себе для піддиректорій
# Якщо знаходить файл, передає його у функцію copy_file

def read_folder(path: Path) -> None:
    try:
        for el in path.iterdir():  # Перебираємо всі елементи в поточній директорії
            if el.is_dir():  # Якщо це папка, обробляємо її рекурсивно
                read_folder(el)
            else:  # Якщо це файл, копіюємо його
                copy_file(el)
    except Exception as e:
        print(f"Помилка під час обробки директорії {path}: {e}")

# Функція для копіювання файлів у директорію призначення
# Файли сортуються за розширеннями у відповідні папки

def copy_file(file: Path) -> None:
    try:
        # Отримуємо розширення файлу або "no_extension", якщо розширення відсутнє
        ext = file.suffix[1:] if file.suffix else "no_extension"
        new_path = output_folder / ext  # Створюємо шлях для папки за розширенням
        new_path.mkdir(exist_ok=True, parents=True)  # Створюємо папку, якщо вона ще не існує

        # Перевіряємо, чи існує файл із таким ім'ям, щоб уникнути конфліктів
        destination_file = new_path / file.name
        counter = 1
        while destination_file.exists():
            # Додаємо номер до назви файлу, якщо він уже існує
            destination_file = new_path / f"{file.stem}_{counter}{file.suffix}"
            counter += 1

        # Копіюємо файл у нову папку
        copyfile(file, destination_file)
        print(f"Copied {file} to {destination_file}")
    except Exception as e:
        print(f"Помилка під час копіювання файлу {file}: {e}")

# Створення директорії призначення, якщо її ще немає
try:
    output_folder.mkdir(exist_ok=True, parents=True)
except Exception as e:
    print(f"Помилка під час створення директорії призначення {output_folder}: {e}")
    exit(1)

# Запуск рекурсивного читання вихідної папки
read_folder(source_folder)