# -*- coding: utf-8 -*-
import subprocess
import datetime
import re
from collections import defaultdict


def get_total_memory():
    """Получить общий объем памяти системы (в МБ)."""
    result = subprocess.Popen(['free', '-m'], stdout=subprocess.PIPE)
    output, _ = result.communicate()
    lines = output.splitlines()
    total_memory = int(lines[1].split()[1])
    return total_memory


def get_cpu_cores():
    """Получить количество доступных ядер процессора."""
    result = subprocess.Popen(['nproc'], stdout=subprocess.PIPE)
    output, _ = result.communicate()
    return int(output.strip())


def get_process_info():
    """Получить список процессов с помощью команды `ps aux`."""
    process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    stdout, _ = process.communicate()
    return stdout.decode('utf-8', errors='ignore')


def parse_processes(ps_output, total_memory, total_cpu_cores):
    """Разобрать данные о процессах."""
    lines = ps_output.splitlines()
    headers = lines[0]
    process_lines = lines[1:]

    users = defaultdict(int)  # Словарь с автоматическим значением 0 для новых ключей
    total_memory_used = 0.0
    total_cpu_used = 0.0
    max_memory_process = ("", 0.0)
    max_cpu_process = ("", 0.0)
    max_cpu_cores = 0.0

    for line in process_lines:
        parts = re.split(r'\s+', line, maxsplit=10)
        if len(parts) < 11:
            continue

        try:
            user, cpu, mem, command = parts[0], float(parts[2]), float(parts[3]), parts[10]
        except ValueError:
            continue

        users[user] += 1  # Увеличиваем счетчик процессов для пользователя

        total_memory_used += mem
        total_cpu_used += cpu

        if mem > max_memory_process[1]:
            max_memory_process = (command[:20], mem)
        if cpu > max_cpu_process[1]:
            max_cpu_process = (command[:20], cpu)
            max_cpu_cores = cpu / 100 * total_cpu_cores

    total_memory_percent = (total_memory_used / total_memory) * 100
    total_cpu_percent = (total_cpu_used / (total_cpu_cores * 100)) * 100

    max_memory_percent = (max_memory_process[1] / total_memory) * 100
    max_cpu_percent = (max_cpu_process[1] / total_cpu_cores) * 100

    return {
        "users": users,
        "total_processes": len(process_lines),
        "total_memory_percent": total_memory_percent,
        "total_cpu_percent": total_cpu_percent,
        "max_memory_process": max_memory_process,
        "max_cpu_process": max_cpu_process,
        "max_memory_percent": max_memory_percent,
        "max_cpu_percent": max_cpu_percent,
        "max_cpu_cores": max_cpu_cores
    }


def generate_report(stats):
    """Создать текст отчета о системе."""
    report = [
        "Отчёт о состоянии системы:",
        "Пользователи системы: {}".format(", ".join(stats["users"].keys())),
        "Процессов запущено: {}".format(stats["total_processes"]),
        "",
        "Пользовательских процессов:",
    ]

    for user, count in stats["users"].items():
        report.append("{}: {}".format(user, count))

    report.extend([
        "",
        "Всего памяти используется: {:.1f}%".format(stats["total_memory_percent"]),
        "Всего CPU используется: {:.1f}%".format(stats["total_cpu_percent"]),
        "Больше всего памяти использует: {:.1f}% ({})".format(stats["max_memory_percent"], stats["max_memory_process"][0]),
        "Больше всего CPU использует: {:.1f}% ({}, используемые ядра: {:.2f})".format(
            stats["max_cpu_percent"], stats["max_cpu_process"][0], stats["max_cpu_cores"]
        ),
    ])

    return "\n".join(report)


def save_report(report_text):
    """Сохранить отчет в файл с меткой времени."""
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = "{}-scan.txt".format(timestamp)

    with open(filename, "w") as f:
        f.write(report_text)

    print("Отчёт сохранён в файл: {}".format(filename))


def main():
    """Основная логика программы."""
    total_memory = get_total_memory()
    total_cpu_cores = get_cpu_cores()

    ps_output = get_process_info()
    stats = parse_processes(ps_output, total_memory, total_cpu_cores)

    report_text = generate_report(stats)
    print(report_text)
    save_report(report_text)


if __name__ == "__main__":
    main()