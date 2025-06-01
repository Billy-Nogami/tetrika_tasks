import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from collections import defaultdict


def get_animal_counts():

    base_url = "https://ru.wikipedia.org"
    start_url = f"{base_url}/wiki/Категория:Животные_по_алфавиту"
    counts = defaultdict(int)
    # Только русские буквы (включая Ё)
    russian_letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    current_url = start_url
    page_num = 1
    while current_url:
        print(f"Обработка страницы #{page_num}: {current_url}")
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Находим основной блок с животными, я немного схитрил и посмотрел html код страницы)))
            category_div = soup.find("div", class_="mw-category-columns")
            if not category_div:
                print("Блок с животными не найден!")
                break
            # Обрабатываем каждую группу животных (по буквам)
            for group in category_div.find_all("div", class_="mw-category-group"):
                # Получаем букву группы
                letter_tag = group.find("h3")
                if not letter_tag:
                    continue
                letter = letter_tag.text.strip()
                # Фильтруем только русские буквы
                if letter in russian_letters:
                    animal_links = group.find_all("a")
                    count = len(animal_links)
                    counts[letter] += count
                else:
                    continue
            # Ищем ссылку на следующую страницу
            next_page_link = None
            for a in soup.find_all("a"):
                if a.text.strip() == "Следующая страница":
                    next_page_link = a.get("href")
                    break
            current_url = urljoin(base_url, next_page_link) if next_page_link else None
            page_num += 1
        except Exception as e:
            print(f"Ошибка: {e}")
            break
    return counts


def save_to_csv(counts):
    os.makedirs("tetrika_tasks/task2", exist_ok=True)
    file_path = "tetrika_tasks/task2/beasts.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
            if counts[letter] > 0:
                f.write(f"{letter},{counts[letter]}\n")
    print(f"Файл сохранен: {file_path}")
    return file_path


if __name__ == "__main__":
    animal_counts = get_animal_counts()
    print("\nРезультаты подсчета:")
    total = 0
    for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        count = animal_counts[letter]
        if count > 0:
            print(f"{letter}: {count}")
            total += count
    print(f"Всего животных (только русские буквы): {total}")
    save_to_csv(animal_counts)
