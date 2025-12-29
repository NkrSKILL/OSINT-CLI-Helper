#!/usr/bin/env python3
"""
Универсальный CLI-помощник для OSINT (Open Source Intelligence)
Версия: 1.0
Автор: NKR_Proger///Tigran Avanesyan
"""

import argparse
import requests
import json
import re
import socket
import whois
import dns.resolver
import subprocess
import sys
import os
from datetime import datetime
from urllib.parse import urlparse
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import ipaddress

# Цвета ANSI
GREEN = "\033[38;2;0;255;0m"
CYAN = "\033[38;2;0;255;255m"
RED = "\033[38;2;255;0;0m"
RESET = "\033[0m"

class Colors:
    """Цвета для вывода в консоль"""
    HEADER = CYAN
    OKBLUE = CYAN
    OKCYAN = CYAN
    OKGREEN = GREEN
    WARNING = RED
    FAIL = RED
    ENDC = RESET
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class OSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def print_banner(self):
        """Вывод масштабного баннера"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{CYAN}")
        print(r'''
  ___  ____  ___ _____ _______   __
 / _ \/ __ \/ _ /_  _/ __/ _ | / /
/ , _/ /_/ / __ |/ // _// __ |/ / \
\_/|_|\____/_/ |_/___/___/_/ |_/  
  / __/ / / / __ \/ |/ / _ \/ _ \
 _\ \/ /_/ / /_/ /    / // / , _/
/___/\____/\____/_/|_/____/_/|_| v1.0
''')
        print(f"{RESET}")
        print(f"{CYAN}{'='*60}{RESET}")
        print(f"{GREEN}{'OSINT CLI by NKR_Coder / Tigran Avanesyan'.center(60)}{RESET}")
        print(f"{CYAN}{'='*60}{RESET}")
    
    def print_section(self, title):
        """Вывод заголовка секции"""
        print(f"{CYAN}=== {title} ==={RESET}")
    
    def print_info(self, message):
        """Вывод информационного сообщения"""
        print(f"{GREEN}{message}{RESET}")
    
    def print_warning(self, message):
        """Вывод предупреждения"""
        print(f"{RED}[WARNING] {message}{RESET}")
    
    def print_error(self, message):
        """Вывод ошибки"""
        print(f"{RED}[ERROR]{RESET} {message}")
    
    def print_result(self, title, data):
        """Вывод результата"""
        print(f"{CYAN}{title}:{RESET} {data}")

    def domain_info(self, domain):
        """Получение информации о домене"""
        self.print_section("АНАЛИЗ ДОМЕНА")
        
        try:
            # WHOIS информация
            self.print_info("Получение WHOIS информации...")
            w = whois.whois(domain)
            
            if w.domain_name:
                self.print_result("Домен", w.domain_name)
            if w.registrar:
                self.print_result("Регистратор", w.registrar)
            if w.creation_date:
                self.print_result("Дата создания", w.creation_date)
            if w.expiration_date:
                self.print_result("Дата истечения", w.expiration_date)
            if w.name_servers:
                self.print_result("NS серверы", w.name_servers)
            
            # DNS записи
            self.print_info("Получение DNS записей...")
            
            # A записи
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                ips = [str(record) for record in a_records]
                self.print_result("A записи (IP адреса)", ", ".join(ips))
            except Exception as e:
                self.print_warning(f"Не удалось получить A записи: {e}")
            
            # MX записи
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                mx_list = [f"{record.exchange} (приоритет: {record.preference})" for record in mx_records]
                self.print_result("MX записи", ", ".join(mx_list))
            except Exception as e:
                self.print_warning(f"Не удалось получить MX записи: {e}")
            
            # TXT записи
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                txt_list = [str(record) for record in txt_records]
                self.print_result("TXT записи", ", ".join(txt_list))
            except Exception as e:
                self.print_warning(f"Не удалось получить TXT записи: {e}")
                
        except Exception as e:
            self.print_error(f"Ошибка при получении информации о домене: {e}")

    def ip_info(self, ip):
        """Получение информации об IP адресе"""
        self.print_section("АНАЛИЗ IP АДРЕСА")
        
        try:
            # Проверка валидности IP
            ipaddress.ip_address(ip)
            
            # Геолокация
            self.print_info("Получение геолокации...")
            response = self.session.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.print_result("Страна", data.get('country', 'N/A'))
                    self.print_result("Город", data.get('city', 'N/A'))
                    self.print_result("Регион", data.get('regionName', 'N/A'))
                    self.print_result("Провайдер", data.get('isp', 'N/A'))
                    self.print_result("Организация", data.get('org', 'N/A'))
                    self.print_result("Координаты", f"{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
                    self.print_result("Часовой пояс", data.get('timezone', 'N/A'))
            
            # Обратный DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                self.print_result("Обратный DNS", hostname)
            except Exception as e:
                self.print_warning(f"Не удалось получить обратный DNS: {e}")
            
            # Проверка портов
            self.print_info("Сканирование популярных портов...")
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
            open_ports = []
            
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    return port if result == 0 else None
                except:
                    return None
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(check_port, common_ports))
                open_ports = [port for port in results if port is not None]
            
            if open_ports:
                self.print_result("Открытые порты", ", ".join(map(str, open_ports)))
            else:
                self.print_result("Открытые порты", "Не найдено")
                
        except Exception as e:
            self.print_error(f"Ошибка при анализе IP: {e}")

    def email_analysis(self, email):
        """Анализ email адреса"""
        self.print_section("АНАЛИЗ EMAIL")
        
        try:
            # Извлечение домена
            domain = email.split('@')[1]
            self.print_result("Email", email)
            self.print_result("Домен", domain)
            
            # Проверка MX записей
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                mx_list = [str(record.exchange) for record in mx_records]
                self.print_result("MX серверы", ", ".join(mx_list))
            except Exception as e:
                self.print_warning(f"Не удалось получить MX записи: {e}")
            
            # Проверка SPF записи
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                spf_records = [str(record) for record in txt_records if 'spf' in str(record).lower()]
                if spf_records:
                    self.print_result("SPF записи", ", ".join(spf_records))
                else:
                    self.print_warning("SPF записи не найдены")
            except Exception as e:
                self.print_warning(f"Не удалось получить SPF записи: {e}")
                
        except Exception as e:
            self.print_error(f"Ошибка при анализе email: {e}")

    def social_media_search(self, username):
        """Поиск пользователя в социальных сетях"""
        self.print_section("ПОИСК В СОЦИАЛЬНЫХ СЕТЯХ")
        
        platforms = {
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Facebook': f'https://facebook.com/{username}',
            'LinkedIn': f'https://linkedin.com/in/{username}',
            'GitHub': f'https://github.com/{username}',
            'YouTube': f'https://youtube.com/@{username}',
            'TikTok': f'https://tiktok.com/@{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'Telegram': f'https://t.me/{username}',
            'VK': f'https://vk.com/{username}'
        }
        
        found_profiles = []
        
        for platform, url in platforms.items():
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    found_profiles.append(platform)
                    self.print_result(platform, url)
                time.sleep(0.5)  # Задержка между запросами
            except Exception as e:
                continue
        
        if found_profiles:
            self.print_info(f"Найдено профилей: {len(found_profiles)}")
        else:
            self.print_warning("Профили не найдены")

    def website_analysis(self, url):
        """Анализ веб-сайта"""
        self.print_section("АНАЛИЗ ВЕБ-САЙТА")
        
        try:
            # Парсинг URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            self.print_result("URL", url)
            self.print_result("Домен", domain)
            self.print_result("Протокол", parsed_url.scheme)
            self.print_result("Путь", parsed_url.path)
            
            # Получение заголовков
            self.print_info("Получение HTTP заголовков...")
            response = self.session.get(url, timeout=10)
            
            self.print_result("Статус код", response.status_code)
            self.print_result("Сервер", response.headers.get('Server', 'N/A'))
            self.print_result("Content-Type", response.headers.get('Content-Type', 'N/A'))
            self.print_result("X-Powered-By", response.headers.get('X-Powered-By', 'N/A'))
            
            # Поиск технологий
            technologies = []
            headers = str(response.headers).lower()
            content = response.text.lower()
            
            tech_patterns = {
                'WordPress': ['wordpress', 'wp-content'],
                'Drupal': ['drupal'],
                'Joomla': ['joomla'],
                'Laravel': ['laravel'],
                'Django': ['django'],
                'React': ['react', 'reactjs'],
                'Angular': ['angular'],
                'Vue.js': ['vue'],
                'Bootstrap': ['bootstrap'],
                'jQuery': ['jquery'],
                'PHP': ['php'],
                'ASP.NET': ['asp.net', 'aspx'],
                'Node.js': ['node.js', 'express'],
                'Nginx': ['nginx'],
                'Apache': ['apache'],
                'IIS': ['iis'],
                'CloudFlare': ['cloudflare'],
                'CDN': ['cdn']
            }
            
            for tech, patterns in tech_patterns.items():
                for pattern in patterns:
                    if pattern in headers or pattern in content:
                        technologies.append(tech)
                        break
            
            if technologies:
                self.print_result("Обнаруженные технологии", ", ".join(set(technologies)))
            
            # Поиск email адресов
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, response.text)
            if emails:
                unique_emails = list(set(emails))[:5]  # Первые 5 уникальных
                self.print_result("Найденные email", ", ".join(unique_emails))
            
            # Поиск телефонных номеров
            phone_pattern = r'[\+]?[1-9][\d]{0,15}'
            phones = re.findall(phone_pattern, response.text)
            if phones:
                unique_phones = list(set(phones))[:5]  # Первые 5 уникальных
                self.print_result("Найденные телефоны", ", ".join(unique_phones))
                
        except Exception as e:
            self.print_error(f"Ошибка при анализе сайта: {e}")

    def breach_check(self, email):
        """Проверка email в утечках данных"""
        self.print_section("ПРОВЕРКА УТЕЧЕК ДАННЫХ")
        
        try:
            # Используем API HaveIBeenPwned (требует API ключ)
            # Для демонстрации показываем формат
            self.print_info("Проверка через HaveIBeenPwned API...")
            self.print_warning("Для полной проверки требуется API ключ от HaveIBeenPwned")
            self.print_result("Email для проверки", email)
            self.print_info("Рекомендуемые сервисы для проверки:")
            self.print_info("- HaveIBeenPwned (haveibeenpwned.com)")
            self.print_info("- DeHashed (dehashed.com)")
            self.print_info("- Intelligence X (intelx.io)")
            
        except Exception as e:
            self.print_error(f"Ошибка при проверке утечек: {e}")

    def subdomain_enumeration(self, domain):
        """Перечисление поддоменов"""
        self.print_section("ПЕРЕЧИСЛЕНИЕ ПОДДОМЕНОВ")
        
        try:
            # Список популярных поддоменов
            common_subdomains = [
                'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test', 'staging',
                'api', 'cdn', 'static', 'img', 'images', 'media', 'files',
                'support', 'help', 'docs', 'wiki', 'forum', 'shop', 'store',
                'app', 'mobile', 'web', 'secure', 'login', 'portal', 'dashboard'
            ]
            
            found_subdomains = []
            
            def check_subdomain(subdomain):
                try:
                    full_domain = f"{subdomain}.{domain}"
                    socket.gethostbyname(full_domain)
                    return full_domain
                except:
                    return None
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                results = list(executor.map(check_subdomain, common_subdomains))
                found_subdomains = [subdomain for subdomain in results if subdomain]
            
            if found_subdomains:
                self.print_result("Найденные поддомены", "\n".join(found_subdomains))
            else:
                self.print_warning("Поддомены не найдены")
                
        except Exception as e:
            self.print_error(f"Ошибка при перечислении поддоменов: {e}")

    def metadata_extraction(self, file_path):
        """Извлечение метаданных из файлов"""
        self.print_section("ИЗВЛЕЧЕНИЕ МЕТАДАННЫХ")
        
        try:
            if not os.path.exists(file_path):
                self.print_error("Файл не найден")
                return
            
            # Для изображений
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                try:
                    from PIL import Image
                    from PIL.ExifTags import TAGS
                    
                    image = Image.open(file_path)
                    exif_data = image._getexif()
                    
                    if exif_data:
                        self.print_info("EXIF данные:")
                        for tag_id in exif_data:
                            tag = TAGS.get(tag_id, tag_id)
                            data = exif_data.get(tag_id)
                            self.print_result(tag, data)
                    else:
                        self.print_warning("EXIF данные не найдены")
                        
                except ImportError:
                    self.print_warning("Для извлечения EXIF данных установите Pillow: pip install Pillow")
                except Exception as e:
                    self.print_error(f"Ошибка при извлечении EXIF: {e}")
            
            # Базовая информация о файле
            stat_info = os.stat(file_path)
            self.print_result("Размер", f"{stat_info.st_size} байт")
            self.print_result("Создан", datetime.fromtimestamp(stat_info.st_ctime))
            self.print_result("Изменен", datetime.fromtimestamp(stat_info.st_mtime))
            
        except Exception as e:
            self.print_error(f"Ошибка при извлечении метаданных: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Универсальный CLI-помощник для OSINT',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python osint_cli.py domain example.com
  python osint_cli.py ip 8.8.8.8
  python osint_cli.py email user@example.com
  python osint_cli.py social username
  python osint_cli.py website https://example.com
  python osint_cli.py breach user@example.com
  python osint_cli.py subdomains example.com
  python osint_cli.py metadata file.jpg
        """
    )
    
    parser.add_argument('command', choices=[
        'domain', 'ip', 'email', 'social', 'website', 
        'breach', 'subdomains', 'metadata'
    ], help='Команда для выполнения')
    
    parser.add_argument('target', help='Цель для анализа')
    
    args = parser.parse_args()
    
    tool = OSINTTool()
    tool.print_banner()
    
    if args.command == 'domain':
        tool.domain_info(args.target)
    elif args.command == 'ip':
        tool.ip_info(args.target)
    elif args.command == 'email':
        tool.email_analysis(args.target)
    elif args.command == 'social':
        tool.social_media_search(args.target)
    elif args.command == 'website':
        tool.website_analysis(args.target)
    elif args.command == 'breach':
        tool.breach_check(args.target)
    elif args.command == 'subdomains':
        tool.subdomain_enumeration(args.target)
    elif args.command == 'metadata':
        tool.metadata_extraction(args.target)

if __name__ == "__main__":
    main() 