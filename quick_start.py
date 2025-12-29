#!/usr/bin/env python3
"""
Быстрый запуск OSINT CLI Helper
Простой интерфейс для начинающих пользователей
"""

import sys
import time
import threading
import os
from osint_advanced import AdvancedOSINT

# Цвета ANSI
GREEN = "\033[38;2;0;255;0m"
CYAN = "\033[38;2;0;255;255m"
RED = "\033[38;2;255;0;0m"
RESET = "\033[0m"

# Анимация текста
def typewriter(text, color=GREEN, delay=0.01, end="\n"):
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    if end:
        print(end, end="")

# Мигающий курсор
stop_cursor = False
def blinking_cursor(color=GREEN):
    import itertools
    for c in itertools.cycle(['_', ' ']):
        if stop_cursor:
            break
        sys.stdout.write(f"\r{color}{c}{RESET}")
        sys.stdout.flush()
        time.sleep(0.5)

# Звуковой эффект
def beep():
    print('\a', end='')

# Новый баннер
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner_art = r'''
⠄⢀⣀⣠⣤⣴⣶⣶⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⢰⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⢸⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⣀⣀⣀⡀⠄⠄
⢸⣿⣿⣿⣿⡿⢿⣿⣤⡀⠄⠄⠄⠄⠄⠄⠄⣠⠴⠚⠋⠉⠉⠉⠙⠂⠄
⢸⣿⣿⣿⠷⢶⣶⣶⣾⣭⣓⠦⠄⠄⠄⠄⠈⣀⣴⣶⣿⠿⠿⠛⠛⠶⣄
⢸⣿⣿⣇⠄⠄⠄⠈⠙⠻⣿⣷⠄⠄⠄⠄⠸⢿⠟⠉⠄⠄⠄⠄⠄⠄⠄
⢸⣿⣿⣿⡄⠄⠄⠄⠄⠄⠈⢻⣦⠄⠄⠄⠰⠃⠄⠄⠄⠄⠄⠄⠄⠄⣠
⢸⣿⡿⠛⠿⠿⠿⠿⠿⢗⣿⣿⣿⣇⠄⠄⠄⠄⠄⠰⠶⠿⠿⠿⠟⠚⠯
⠄⣿⠄⠄⠄⠄⠄⠄⠄⠁⣾⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⣿⠄⠄⠄⠄⠄⠄⠄⣰⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⣿⠄⠄⠄⠄⠄⠄⢠⣿⣿⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⢹⡦⢄⣀⣠⣤⠖⠛⠛⠿⣿⣿⡅⠄⠄⢀⣀⠄⠄⠈⠓⠦⣄⣀⣠⠄
⠄⠘⣿⡀⢹⡿⣧⡀⠄⠄⠄⠈⣹⣿⣶⣾⣧⡀⠄⠄⠄⢀⣠⡾⢡⠏
⠄⠄⠹⣷⠈⣷⡙⢿⣷⣶⣶⣾⣿⠟⠁⠻⣿⣿⣶⣶⣶⡿⠟⢀⡾
⠄⠄⠄⠹⣧⡘⢷⡀⠄⠄⠄⠠⠤⠤⠤⠤⠤⠄⠄⠄⠄⠄⢠⡞
⠄⠄⠄⠄⠘⢷⡌⠳⡀⠄⠄⠄⠠⣤⣤⣤⡤⠄⠄⠄⠄⣰⠋
⠄⠄⠄⠄⠄⠄⠻⣆⠙⡄⠄⠄⠄⠈⣿⣿⠁⠄⠄⠄⠔⠁
⠄⠄⠄⠄⠄⠄⠄⠘⢧⡈⠂⠄⠄⢰⣿⣿⡆⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠻⣄⠄⠄⠸⣿⣿⡇⠄
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠂⠄⠄⣿⣿⠁
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠸⠇
'''
    typewriter(banner_art, CYAN, 0.002)
    print(f"{CYAN}{'='*60}{RESET}")
    typewriter("OSINT CLI by NKR_Coder / Tigran Avanesyan".center(60), GREEN, 0.002)
    print(f"{CYAN}{'='*60}{RESET}")

def print_menu():
    print(f"""
{'═'*60}
{' '*15} ГЛАВНОЕ МЕНЮ
{'═'*60}

 ОСНОВНЫЕ ВОЗМОЖНОСТИ:
  1.   Анализ домена
  2.   Анализ IP-адреса  
  3.   Анализ email-адреса
  4.   Поиск в социальных сетях
  5.   Анализ веб-сайта
  6.   Проверка утечек данных
  7.   Перечисление поддоменов
  8.   Извлечение метаданных
  9.   Расширенные возможности
  0.   Выход
{'═'*60}
""")

def main():
    from osint_cli import OSINTTool
    tool = OSINTTool()
    tool.print_banner()
    while True:
        print_menu()
        choice = input("Введите номер (0-9): ").strip()
        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            domain = input("Введите домен (например: example.com): ").strip()
            if domain:
                tool.domain_info(domain)
        elif choice == "2":
            ip = input("Введите IP-адрес (например: 8.8.8.8): ").strip()
            if ip:
                tool.ip_info(ip)
        elif choice == "3":
            email = input("Введите email-адрес: ").strip()
            if email:
                tool.email_analysis(email)
        elif choice == "4":
            username = input("Введите username: ").strip()
            if username:
                tool.social_media_search(username)
        elif choice == "5":
            url = input("Введите URL сайта: ").strip()
            if url:
                tool.website_analysis(url)
        elif choice == "6":
            email = input("Введите email для проверки: ").strip()
            if email:
                tool.breach_check(email)
        elif choice == "7":
            domain = input("Введите домен для поиска поддоменов: ").strip()
            if domain:
                tool.subdomain_enumeration(domain)
        elif choice == "8":
            file_path = input("Введите путь к файлу: ").strip()
            if file_path:
                tool.metadata_extraction(file_path)
        elif choice == "9":
            advanced = AdvancedOSINT()
            print("\nРасширенные возможности:")
            print("1. Shodan поиск")
            print("2. Wayback Machine")
            print("3. Google Dorks")
            print("4. Certificate Transparency")
            print("5. Threat Intelligence")
            print("6. Расширенный поиск в соцсетях")
            print("7. Проверка репутации домена")
            print("8. Сканирование сети")
            adv_choice = input("\nВыберите функцию (1-8): ")
            target = input("Введите цель: ")
            if adv_choice == "1":
                api_key = input("Введите API ключ Shodan (или Enter для пропуска): ")
                advanced.shodan_search(target, api_key if api_key else None)
            elif adv_choice == "2":
                advanced.wayback_machine(target)
            elif adv_choice == "3":
                advanced.google_dorks(target)
            elif adv_choice == "4":
                advanced.certificate_transparency(target)
            elif adv_choice == "5":
                advanced.threat_intelligence(target)
            elif adv_choice == "6":
                advanced.social_media_advanced(target)
            elif adv_choice == "7":
                advanced.domain_reputation(target)
            elif adv_choice == "8":
                advanced.network_scan(target)
            else:
                print("Неверный выбор")
        else:
            print("Неверный выбор. Попробуйте снова.")
        input("\nНажмите Enter для продолжения...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main() 