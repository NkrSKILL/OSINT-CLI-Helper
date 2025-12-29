# Примеры использования OSINT CLI Helper

## Быстрый старт

### 1. Интерактивный режим
```bash
python quick_start.py
```

### 2. Командная строка
```bash
python osint_cli.py <команда> <цель>
```

## Подробные примеры

### Анализ домена

#### Базовый анализ
```bash
python osint_cli.py domain google.com
```

**Результат:**
- WHOIS информация (регистратор, даты)
- DNS записи (A, MX, TXT)
- NS серверы

#### Перечисление поддоменов
```bash
python osint_cli.py subdomains google.com
```

**Результат:**
- Список найденных поддоменов
- Статус доступности

### Анализ IP-адреса

#### Геолокация и информация
```bash
python osint_cli.py ip 8.8.8.8
```

**Результат:**
- Страна, город, провайдер
- Координаты
- Обратный DNS
- Открытые порты

#### Сканирование сети (расширенный)
```bash
python osint_advanced.py
# Выберите опцию 8
# Введите: 192.168.1.0/24
```

### Анализ email-адреса

#### Проверка домена
```bash
python osint_cli.py email admin@example.com
```

**Результат:**
- MX серверы домена
- SPF записи
- Рекомендации по безопасности

#### Проверка утечек
```bash
python osint_cli.py breach user@example.com
```

### Поиск в социальных сетях

#### Поиск профилей
```bash
python osint_cli.py social john_doe
```

**Результат:**
- Найденные профили на платформах:
  - Twitter, Instagram, Facebook
  - LinkedIn, GitHub, YouTube
  - TikTok, Reddit, Telegram, VK

#### Расширенный поиск
```bash
python osint_advanced.py
# Выберите опцию 6
# Введите username
```

**Дополнительные платформы:**
- Snapchat, Pinterest, Tumblr
- Medium, DeviantArt, Steam
- Twitch, Discord, Stack Overflow
- Behance, Dribbble, Flickr
- SoundCloud, Spotify, Last.fm

### Анализ веб-сайта

#### Технический анализ
```bash
python osint_cli.py website https://example.com
```

**Результат:**
- HTTP заголовки
- Обнаруженные технологии
- Email адреса и телефоны
- Структура сайта

### Извлечение метаданных

#### Из изображений
```bash
python osint_cli.py metadata photo.jpg
```

**Результат:**
- EXIF данные (GPS, камера, дата)
- Размер файла
- Временные метки

## Расширенные возможности

### Wayback Machine
```bash
python osint_advanced.py
# Выберите опцию 2
# Введите: example.com
```

### Google Dorks
```bash
python osint_advanced.py
# Выберите опцию 3
# Введите: example.com
```

**Сгенерированные dorks:**
- `site:example.com filetype:pdf`
- `site:example.com inurl:admin`
- `site:example.com "index of"`
- `site:example.com ext:php`

### Certificate Transparency
```bash
python osint_advanced.py
# Выберите опцию 4
# Введите: example.com
```

### Threat Intelligence
```bash
python osint_advanced.py
# Выберите опцию 5
# Введите: example.com
```

## Комбинированные сценарии

### Полный анализ домена
```bash
# 1. Базовая информация
python osint_cli.py domain example.com

# 2. Поддомены
python osint_cli.py subdomains example.com

# 3. Wayback Machine
python osint_advanced.py
# Выберите 2, введите example.com

# 4. Google Dorks
python osint_advanced.py
# Выберите 3, введите example.com

# 5. Certificate Transparency
python osint_advanced.py
# Выберите 4, введите example.com
```

### Анализ организации
```bash
# 1. Основной домен
python osint_cli.py domain company.com

# 2. Поиск сотрудников в соцсетях
python osint_cli.py social company_name

# 3. Анализ веб-сайта
python osint_cli.py website https://company.com

# 4. Проверка репутации
python osint_advanced.py
# Выберите 7, введите company.com
```

### Исследование угроз
```bash
# 1. Проверка IP
python osint_cli.py ip 192.168.1.100

# 2. Threat Intelligence
python osint_advanced.py
# Выберите 5, введите IP или домен

# 3. Shodan поиск (с API ключом)
python osint_advanced.py
# Выберите 1, введите запрос
```

## Полезные советы

### 1. Сохранение результатов
```bash
# Перенаправление вывода в файл
python osint_cli.py domain example.com > results.txt

# С дополнительной информацией
python osint_cli.py domain example.com 2>&1 | tee results.txt
```

### 2. Пакетный анализ
```bash
# Создайте файл targets.txt:
# example1.com
# example2.com
# example3.com

# Скрипт для пакетного анализа
for target in $(cat targets.txt); do
    echo "Анализ $target..."
    python osint_cli.py domain $target
    echo "---"
done
```

### 3. Использование API ключей
```bash
# Для Shodan
export SHODAN_API_KEY="your_api_key_here"

# Для VirusTotal
export VIRUSTOTAL_API_KEY="your_api_key_here"
```

### 4. Настройка прокси
```bash
# В коде добавьте:
# self.session.proxies = {
#     'http': 'http://proxy:port',
#     'https': 'https://proxy:port'
# }
```

## Обработка ошибок

### Частые проблемы и решения

1. **Ошибка DNS**
   - Проверьте интернет-соединение
   - Попробуйте другой DNS сервер

2. **Таймаут запросов**
   - Увеличьте timeout в коде
   - Используйте VPN

3. **Блокировка IP**
   - Используйте прокси
   - Добавьте задержки между запросами

4. **Ошибки API**
   - Проверьте API ключи
   - Убедитесь в лимитах запросов

## Безопасность

### Рекомендации
- Используйте только для этичных целей
- Получайте разрешение перед анализом
- Соблюдайте законы о защите данных
- Не превышайте разумные лимиты запросов

### Ограничения
- Некоторые API требуют регистрации
- Бесплатные API имеют лимиты
- Некоторые сервисы могут блокировать запросы 