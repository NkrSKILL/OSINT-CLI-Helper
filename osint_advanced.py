#!/usr/bin/env python3
"""
Расширенный модуль для OSINT CLI Helper
Дополнительные возможности для углубленного анализа
"""

import requests
import json
import re
import time
import hashlib
import base64
import socket
import ipaddress
from urllib.parse import urljoin, urlparse
import threading
from concurrent.futures import ThreadPoolExecutor
import os

class AdvancedOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def print_section(self, title):
        """Вывод заголовка секции"""
        print(f"\n\033[94m\033[1m=== {title} ===\033[0m")
    
    def print_info(self, message):
        """Вывод информационного сообщения"""
        print(f"\033[92m[INFO]\033[0m {message}")
    
    def print_result(self, title, data):
        """Вывод результата"""
        print(f"\033[96m{title}:\033[0m {data}")
    
    def print_error(self, message):
        """Вывод ошибки"""
        print(f"\033[91m[ERROR]\033[0m {message}")
    
    def print_warning(self, message):
        """Вывод предупреждения"""
        print(f"\033[93m[WARNING]\033[0m {message}")

    def shodan_search(self, query, api_key=None):
        """Поиск через Shodan API"""
        self.print_section("ПОИСК ЧЕРЕЗ SHODAN")
        
        if not api_key:
            self.print_info("Для полного поиска требуется API ключ Shodan")
            self.print_info("Получите ключ на: https://account.shodan.io/")
            return
        
        try:
            url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', 0)
                self.print_result("Найдено результатов", total)
                
                for result in data.get('matches', [])[:5]:
                    ip = result.get('ip_str', 'N/A')
                    port = result.get('port', 'N/A')
                    product = result.get('product', 'N/A')
                    self.print_result(f"IP:Port", f"{ip}:{port} ({product})")
            else:
                self.print_error("Ошибка при поиске в Shodan")
                
        except Exception as e:
            self.print_error(f"Ошибка: {e}")

    def wayback_machine(self, domain):
        """Поиск в Wayback Machine"""
        self.print_section("ПОИСК В WAYBACK MACHINE")
        
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={domain}&output=json&fl=original&collapse=urlkey"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:  # Первая строка - заголовки
                    self.print_result("Найдено архивных версий", len(data) - 1)
                    
                    # Показываем первые 10 уникальных URL
                    unique_urls = set()
                    for row in data[1:11]:  # Пропускаем заголовок
                        if row:
                            unique_urls.add(row[0])
                    
                    for url in list(unique_urls)[:5]:
                        self.print_result("Архивный URL", url)
                else:
                    self.print_info("Архивные версии не найдены")
            else:
                self.print_error("Ошибка при поиске в Wayback Machine")
                
        except Exception as e:
            self.print_error(f"Ошибка: {e}")

    def google_dorks(self, domain):
        """Генерация Google Dorks"""
        self.print_section("GOOGLE DORKS")
        
        dorks = [
            f'site:{domain}',
            f'site:{domain} filetype:pdf',
            f'site:{domain} filetype:doc OR filetype:docx',
            f'site:{domain} inurl:admin',
            f'site:{domain} inurl:login',
            f'site:{domain} inurl:wp-admin',
            f'site:{domain} "index of"',
            f'site:{domain} ext:php',
            f'site:{domain} ext:asp',
            f'site:{domain} "error" OR "warning"',
            f'site:{domain} "password" OR "username"',
            f'site:{domain} "@gmail.com" OR "@yahoo.com"',
            f'site:{domain} "phone" OR "tel:"',
            f'site:{domain} "address" OR "location"',
            f'site:{domain} "confidential" OR "private"'
        ]
        
        self.print_info("Сгенерированные Google Dorks:")
        for i, dork in enumerate(dorks, 1):
            print(f"{i:2d}. {dork}")
        
        self.print_info(f"\nВсего сгенерировано: {len(dorks)} dorks")

    def certificate_transparency(self, domain):
        """Поиск в Certificate Transparency logs"""
        self.print_section("CERTIFICATE TRANSPARENCY")
        
        try:
            # Используем crt.sh API
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.print_result("Найдено сертификатов", len(data))
                    
                    # Показываем уникальные домены
                    unique_domains = set()
                    for cert in data:
                        name_value = cert.get('name_value', '')
                        if name_value:
                            # Разбиваем на отдельные домены
                            domains = name_value.split('\n')
                            for domain_name in domains:
                                if domain_name.strip():
                                    unique_domains.add(domain_name.strip())
                    
                    self.print_result("Уникальных доменов", len(unique_domains))
                    
                    # Показываем первые 10
                    for domain_name in list(unique_domains)[:10]:
                        self.print_result("Домен", domain_name)
                else:
                    self.print_info("Сертификаты не найдены")
            else:
                self.print_error("Ошибка при поиске сертификатов")
                
        except Exception as e:
            self.print_error(f"Ошибка: {e}")

    def threat_intelligence(self, target):
        """Проверка в базах данных угроз"""
        self.print_section("АНАЛИЗ УГРОЗ")
        
        try:
            # VirusTotal API (требует API ключ)
            self.print_info("Проверка в VirusTotal...")
            self.print_info("Для полной проверки требуется API ключ")
            
            # AlienVault OTX (требует API ключ)
            self.print_info("Проверка в AlienVault OTX...")
            self.print_info("Для полной проверки требуется API ключ")
            
            # URLVoid (бесплатный)
            url = f"https://api.urlvoid.com/v1/payload/{target}/"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('response', {}).get('detections', 0) > 0:
                    self.print_result("Статус", "ОБНАРУЖЕНА УГРОЗА")
                    self.print_result("Детекций", data['response']['detections'])
                else:
                    self.print_result("Статус", "УГРОЗ НЕ ОБНАРУЖЕНО")
            else:
                self.print_info("URLVoid недоступен")
                
        except Exception as e:
            self.print_error(f"Ошибка: {e}")

    def social_media_advanced(self, username):
        """Расширенный поиск в социальных сетях"""
        self.print_section("РАСШИРЕННЫЙ ПОИСК В СОЦСЕТЯХ")
        
        # Дополнительные платформы
        platforms = {
            'Snapchat': f'https://snapchat.com/add/{username}',
            'Pinterest': f'https://pinterest.com/{username}',
            'Tumblr': f'https://{username}.tumblr.com',
            'Medium': f'https://medium.com/@{username}',
            'DeviantArt': f'https://deviantart.com/{username}',
            'Steam': f'https://steamcommunity.com/id/{username}',
            'Twitch': f'https://twitch.tv/{username}',
            'Discord': f'https://discord.com/users/{username}',
            'Slack': f'https://{username}.slack.com',
            'Stack Overflow': f'https://stackoverflow.com/users/{username}',
            'Behance': f'https://behance.net/{username}',
            'Dribbble': f'https://dribbble.com/{username}',
            'Flickr': f'https://flickr.com/photos/{username}',
            '500px': f'https://500px.com/{username}',
            'SoundCloud': f'https://soundcloud.com/{username}',
            'Spotify': f'https://open.spotify.com/user/{username}',
            'Last.fm': f'https://last.fm/user/{username}',
            'Goodreads': f'https://goodreads.com/user/show/{username}',
            'Letterboxd': f'https://letterboxd.com/{username}'
        }
        
        found_profiles = []
        
        def check_profile(platform, url):
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    return platform, url
                return None
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_profile, platform, url) 
                      for platform, url in platforms.items()]
            
            for future in futures:
                result = future.result()
                if result:
                    platform, url = result
                    found_profiles.append((platform, url))
                    self.print_result(platform, url)
        
        self.print_result("Всего найдено профилей", len(found_profiles))

    def email_breach_check_advanced(self, email):
        """Расширенная проверка утечек"""
        self.print_section("РАСШИРЕННАЯ ПРОВЕРКА УТЕЧЕК")
        
        # Список сервисов для проверки
        services = [
            "HaveIBeenPwned",
            "DeHashed", 
            "Intelligence X",
            "Leak-Lookup",
            "H8mail",
            "BreachDirectory",
            "Snusbase",
            "LeakCheck"
        ]
        
        self.print_info("Рекомендуемые сервисы для проверки:")
        for i, service in enumerate(services, 1):
            print(f"{i:2d}. {service}")
        
        self.print_info(f"\nEmail для проверки: {email}")
        self.print_info("Для полной проверки используйте специализированные инструменты")

    def domain_reputation(self, domain):
        """Проверка репутации домена"""
        self.print_section("ПРОВЕРКА РЕПУТАЦИИ ДОМЕНА")
        
        try:
            # Проверка в различных сервисах
            checks = [
                ("Google Safe Browsing", f"https://safebrowsing.google.com/safebrowsing/diagnostic?site={domain}"),
                ("Norton Safe Web", f"https://safeweb.norton.com/report/show?url={domain}"),
                ("URLVoid", f"https://www.urlvoid.com/scan/{domain}/"),
                ("VirusTotal", f"https://www.virustotal.com/gui/domain/{domain}"),
                ("Sucuri SiteCheck", f"https://sitecheck.sucuri.net/results/{domain}")
            ]
            
            for service, url in checks:
                self.print_result(service, url)
                
        except Exception as e:
            self.print_error(f"Ошибка: {e}")

    def network_scan(self, target):
        """Сканирование сети"""
        self.print_section("СКАНИРОВАНИЕ СЕТИ")
        
        try:
            # Определяем диапазон IP
            if '/' in target:
                # CIDR нотация
                network = ipaddress.ip_network(target, strict=False)
                ips = list(network.hosts())
            else:
                # Одиночный IP
                ips = [target]
            
            self.print_result("Целей для сканирования", len(ips))
            self.print_info("Начинаю сканирование...")
            
            # Сканируем популярные порты
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
            
            # Словарь с названиями портов
            port_names = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 
                993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP", 
                5432: "PostgreSQL", 8080: "HTTP-Proxy"
            }
            
            def scan_host(ip):
                open_ports = []
                self.print_info(f"Сканирую {ip}...")
                
                for port in common_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)  # Увеличиваем таймаут
                        result = sock.connect_ex((str(ip), port))
                        sock.close()
                        if result == 0:
                            port_name = port_names.get(port, f"Port {port}")
                            open_ports.append((port, port_name))
                    except Exception as e:
                        continue
                
                return str(ip), open_ports
            
            # Сканируем последовательно для лучшего контроля
            results = []
            for ip in ips:
                ip_str, ports = scan_host(ip)
                results.append((ip_str, ports))
            
            # Выводим результаты
            found_hosts = 0
            for ip, ports in results:
                if ports:
                    found_hosts += 1
                    self.print_result(f"IP {ip}", f"Найдено открытых портов: {len(ports)}")
                    for port, name in ports:
                        self.print_result(f"  Порт {port}", f"{name}")
                else:
                    self.print_result(f"IP {ip}", "Открытых портов не найдено")
            
            self.print_result("Активных хостов", found_hosts)
            
            if found_hosts == 0:
                self.print_warning("Активных хостов не найдено. Возможные причины:")
                self.print_warning("- Все порты закрыты")
                self.print_warning("- Брандмауэр блокирует соединения")
                self.print_warning("- Слишком короткий таймаут")
                self.print_info("Попробуйте увеличить таймаут или проверить настройки сети")
                        
        except Exception as e:
            self.print_error(f"Ошибка: {e}")
            self.print_info("Убедитесь, что введен корректный IP-адрес или диапазон")
            self.print_info("Примеры: 127.0.0.1, 192.168.1.0/24")

    def generate_report(self, target, results):
        """Генерация отчета"""
        self.print_section("ГЕНЕРАЦИЯ ОТЧЕТА")
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        report = f"""
OSINT ОТЧЕТ
===========
Цель: {target}
Дата: {timestamp}

РЕЗУЛЬТАТЫ:
{results}

Сгенерировано с помощью OSINT CLI Helper
        """
        
        filename = f"osint_report_{target}_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.print_result("Отчет сохранен", filename)

def main():
    """Демонстрация расширенных возможностей"""
    advanced = AdvancedOSINT()
    
    print("Расширенный OSINT CLI Helper")
    print("Доступные функции:")
    print("1. Shodan поиск")
    print("2. Wayback Machine")
    print("3. Google Dorks")
    print("4. Certificate Transparency")
    print("5. Threat Intelligence")
    print("6. Расширенный поиск в соцсетях")
    print("7. Проверка репутации домена")
    print("8. Сканирование сети")
    
    choice = input("\nВыберите функцию (1-8): ")
    target = input("Введите цель: ")
    
    if choice == "1":
        api_key = input("Введите API ключ Shodan (или Enter для пропуска): ")
        advanced.shodan_search(target, api_key if api_key else None)
    elif choice == "2":
        advanced.wayback_machine(target)
    elif choice == "3":
        advanced.google_dorks(target)
    elif choice == "4":
        advanced.certificate_transparency(target)
    elif choice == "5":
        advanced.threat_intelligence(target)
    elif choice == "6":
        advanced.social_media_advanced(target)
    elif choice == "7":
        advanced.domain_reputation(target)
    elif choice == "8":
        advanced.network_scan(target)
    else:
        print("Неверный выбор")

if __name__ == "__main__":
    main() 