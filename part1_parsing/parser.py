import argparse
import csv
import os
import re
import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

CACHE_DIR = "cache"
REQUEST_TIMEOUT = 10
PAUSE_BETWEEN_REQUESTS = 1


def read_countries(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    countries = [line.strip() for line in lines]
    countries = [c for c in countries if c]
    return countries


def country_to_url(country):
    page_name = country.strip().replace(" ", "_")
    return f"https://en.wikipedia.org/wiki/{page_name}"


def cache_path_for(country):
    safe_name = country.strip().replace(" ", "_")
    return os.path.join(CACHE_DIR, f"{safe_name}.html")


def get_html(country):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = cache_path_for(country)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    url = country_to_url(country)
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    html = response.text
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    time.sleep(PAUSE_BETWEEN_REQUESTS)
    return html


def clean_number(text):
    if not text:
        return ""
    text = re.sub(r"\[.*?\]", "", text)
    match = re.search(r"\d[\d,]*", text)
    if not match:
        return ""
    return match.group().replace(",", "")


def parse_infobox(html):
    soup = BeautifulSoup(html, "html.parser")
    data = {"city": "", "area": "", "population": ""}

    infobox = soup.find("table", class_=re.compile("infobox"))
    if infobox is None:
        return data

    current_section = None

    for row in infobox.find_all("tr"):
        cells = row.find_all(["th", "td"], recursive=False)

        if len(cells) == 1 and cells[0].name == "th":
            current_section = cells[0].get_text(" ", strip=True)
            continue

        if len(cells) == 2:
            first, second = cells
            label = first.get_text(" ", strip=True)
            value_cell = second
            value_text = value_cell.get_text(" ", strip=True)
            value_text_clean = re.sub(r"\[.*?\]", "", value_text)
            label_lower = label.lower()

            if first.name == "th" and not data["city"] and "Capital" in label:
                link = value_cell.find("a")
                raw_city = link.get_text(strip=True) if link else value_text
                raw_city = re.sub(r"\[.*?\]", "", raw_city)
                data["city"] = re.split(r"\d", raw_city)[0].strip().rstrip(", ")
                continue

            if first.name == "th" and not data["area"] and label.startswith("Area"):
                km_match = re.search(r"([\d,]+(?:\.\d+)?)\s*km", value_text_clean)
                if km_match:
                    raw_number = km_match.group(1).replace(",", "")
                    data["area"] = str(round(float(raw_number)))
                continue

            if first.name == "th" and not data["population"] and label.startswith("Population"):
                data["population"] = clean_number(value_text)
                continue

            if current_section == "Area" and not data["area"]:
                stripped_label = label_lower.strip("• ")
                if "total" in label_lower or stripped_label == "":
                    km_match = re.search(r"([\d,]+(?:\.\d+)?)\s*km", value_text_clean)
                    if km_match:
                        raw_number = km_match.group(1).replace(",", "")
                        data["area"] = str(round(float(raw_number)))

            elif current_section == "Population" and not data["population"]:
                if "density" not in label_lower and "%" not in label_lower:
                    data["population"] = clean_number(value_text)

    return data


def collect_country_data(country):
    result = {"country": country, "city": "", "area": "", "population": ""}
    try:
        html = get_html(country)
        parsed = parse_infobox(html)
        result.update(parsed)
    except requests.RequestException as e:
        print(f"[{country}] Ошибка сети: {e}")
    except Exception as e:
        print(f"[{country}] Не удалось получить данные: {e}")
    return result


def write_csv(rows, output_path):
    fieldnames = ["country", "city", "area", "population"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="countries.txt")
    parser.add_argument("--output", default="countries_data.csv")
    args = parser.parse_args()

    countries = read_countries(args.input)
    rows = []
    for country in countries:
        print(f"Обрабатываю: {country}")
        rows.append(collect_country_data(country))

    write_csv(rows, args.output)
    print(f"Готово. Результат сохранён в {args.output}")


if __name__ == "__main__":
    main()