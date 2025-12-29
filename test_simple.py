#!/usr/bin/env python3
"""
Простой тест для проверки работы OSINT CLI
"""

import sys
import os

def main():
    print("=== ТЕСТ OSINT CLI ===")
    print("Python версия:", sys.version)
    print("Текущая директория:", os.getcwd())
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError as e:
        print("❌ requests - ОШИБКА:", e)
    
    try:
        import whois
        print("✅ whois - OK")
    except ImportError as e:
        print("❌ whois - ОШИБКА:", e)
    
    try:
        import dns.resolver
        print("✅ dns - OK")
    except ImportError as e:
        print("❌ dns - ОШИБКА:", e)
    
    try:
        from PIL import Image
        print("✅ PIL - OK")
    except ImportError as e:
        print("❌ PIL - ОШИБКА:", e)
    
    print("\n=== ТЕСТ ЗАВЕРШЕН ===")
    
    # Пауза для Windows
    if os.name == 'nt':
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main() 