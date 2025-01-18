# -*- coding: utf-8 -*-
import os
import re
import json
import argparse
from collections import Counter


def parse_log_line(line):
    """Парсит одну строку лога и извлекает данные."""
    log_pattern = re.compile(
        r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\S+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)" (?P<duration>\d+)'
    )
    match = log_pattern.match(line)
    if not match:
        return None

    data = match.groupdict()
    # Парсим метод, URL и протокол из запроса
    request_parts = data["request"].split()
    if len(request_parts) == 3:
        data["method"], data["url"], data["protocol"] = request_parts
    else:
        data["method"], data["url"], data["protocol"] = None, None, None

    # Преобразуем данные в нужные типы
    data["size"] = int(data["size"]) if data["size"].isdigit() else 0
    data["duration"] = int(data["duration"])
    return data


def process_log_file(file_path):
    """Обрабатывает файл лога и собирает статистику."""
    stats = {
        "total_requests": 0,
        "methods": Counter(),
        "top_ips": Counter(),
        "longest_requests": []
    }

    with open(file_path, "r") as log_file:
        for line in log_file:
            parsed = parse_log_line(line)
            if not parsed:
                continue

            # Общая статистика
            stats["total_requests"] += 1
            stats["methods"][parsed["method"]] += 1
            stats["top_ips"][parsed["ip"]] += 1

            # Обновляем топ-3 долгих запросов
            stats["longest_requests"].append({
                "method": parsed["method"],
                "url": parsed["url"],
                "ip": parsed["ip"],
                "duration": parsed["duration"],
                "time": parsed["time"]
            })
            stats["longest_requests"] = sorted(
                stats["longest_requests"],
                key=lambda x: x["duration"],
                reverse=True
            )[:3]

    return stats


def save_stats_to_json(stats, file_name):
    """Сохраняет статистику в JSON-файл."""
    with open(file_name, "w") as json_file:
        json.dump(stats, json_file, indent=4, ensure_ascii=False)
    print(f"Сохранено в файл: {file_name}")


def main():
    parser = argparse.ArgumentParser(description="Анализ логов веб-сервера.")
    parser.add_argument(
        "path",
        type=str,
        help="Путь до файла лога или директории с логами."
    )
    args = parser.parse_args()

    path = args.path
    if os.path.isfile(path):
        log_files = [path]
    elif os.path.isdir(path):
        log_files = [
            os.path.join(path, f) for f in os.listdir(path)
            if f.endswith(".log")
        ]
    else:
        print("Указан неверный путь.")
        return

    for log_file in log_files:
        print(f"Обработка файла: {log_file}")
        stats = process_log_file(log_file)

        # Сохраняем результат в JSON
        json_file_name = f"{os.path.splitext(log_file)[0]}_stats.json"
        save_stats_to_json(stats, json_file_name)

        # Выводим в терминал
        print(json.dumps(stats, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
