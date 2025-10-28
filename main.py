import os  # Для роботи з файловою системою (отримати список файлів)
import shutil  # Для переміщення файлів
from pathlib import Path  # Для зручної роботи зі шляхами (сучасний спосіб)

# --- Налаштування ---

# 1. Вкажи шлях до папки, яку будемо сортувати.
# ВАЖЛИВО: Заміни 'твій_користувач' на своє ім'я користувача в macOS.
# Або просто скопіюй шлях до папки TEST_FOLDER.
# Наприклад: "/Users/tviy_user/Desktop/TEST_FOLDER"
# Використовуй Path() для коректної роботи на будь-якій ОС.
# Path.home() автоматично знайде твою домашню директорію (/Users/tviy_user)
TARGET_FOLDER = Path.home() / "Desktop" / "TEST_FOLDER"

# 2. Визначимо, куди що класти.
# Ключ словника - це назва папки, яку ми створимо.
# Значення - це список розширень, які туди потраплять.
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt", ".pptx"],
    "Archives": [".zip", ".gz", ".tar", ".rar"],
    "Music": [".mp3", ".wav", ".aac"],
    "Video": [".mov", ".mp4", ".avi", ".mkv"],
}

# Папка для файлів, розширення яких ми не знаємо
OTHER_FOLDER = "Other"


# --- Логіка скрипта ---

def sort_files(folder_path: Path):
    """
    Головна функція, яка сортує файли в заданій папці.
    """
    print(f"--- Починаю сортування в папці: {folder_path} ---")

    # .iterdir() дає нам всі файли і папки всередині
    for item in folder_path.iterdir():

        # 3. Ігноруємо папки, сортуємо тільки файли
        if item.is_dir():
            # Додатково перевіряємо, щоб не чіпати папки,
            # які ми самі створили (Images, Documents тощо)
            if item.name not in CATEGORIES and item.name != OTHER_FOLDER:
                print(f"Знайдено папку, ігнорую: {item.name}")
            continue  # Переходимо до наступного елемента

        # 4. Отримуємо розширення файлу в нижньому регістрі
        # Наприклад, ".JPG" -> ".jpg"
        file_suffix = item.suffix.lower()

        # 5. Якщо у файлу немає розширення (напр. 'myfile'), пропускаємо
        if not file_suffix:
            print(f"Файл без розширення, ігнорую: {item.name}")
            continue

        # 6. Шукаємо, до якої категорії належить файл
        moved = False  # Прапорець, чи перемістили ми файл
        for category_name, suffixes in CATEGORIES.items():
            if file_suffix in suffixes:
                # 7. Знайшли! Створюємо папку для цієї категорії
                category_path = folder_path / category_name
                # exist_ok=True означає "не видавати помилку, якщо папка вже існує"
                category_path.mkdir(exist_ok=True)

                # 8. Переміщуємо файл
                destination = category_path / item.name
                shutil.move(str(item), str(destination))

                print(f"Переміщено: {item.name} -> {category_name}/")
                moved = True
                break  # Виходимо з циклу, бо вже знайшли категорію

        # 9. Якщо файл не потрапив у жодну категорію
        if not moved:
            # Створюємо папку "Other"
            other_path = folder_path / OTHER_FOLDER
            other_path.mkdir(exist_ok=True)

            # Переміщуємо файл туди
            destination = other_path / item.name
            shutil.move(str(item), str(destination))
            print(f"Переміщено (інше): {item.name} -> {OTHER_FOLDER}/")

    print("--- Сортування завершено! ---")


# Це стандартна конструкція, яка запускає наш скрипт,
# якщо ми запускаємо його напряму (а не імпортуємо)
if __name__ == "__main__":
    # Перевіряємо, чи існує папка, яку ми хочемо сортувати
    if not TARGET_FOLDER.exists() or not TARGET_FOLDER.is_dir():
        print(f"ПОМИЛКА: Папка {TARGET_FOLDER} не знайдена.")
        print("Будь ласка, перевір шлях у змінній TARGET_FOLDER в коді.")
    else:
        sort_files(TARGET_FOLDER)