# Используем базовый образ Python с минимальным размером
FROM python:3.9-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    default-jre \
    chromium \
    firefox-esr \
    libnss3 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxrandr2 \
    fonts-liberation \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

# Устанавливаем Geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.35.0-linux64.tar.gz -C /usr/local/bin/ && \
    rm geckodriver-v0.35.0-linux64.tar.gz && \
    chmod +x /usr/local/bin/geckodriver

# Устанавливаем Python-зависимости
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Устанавливаем Allure
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.tgz && \
    tar -xzf allure-2.20.1.tgz -C /opt/ && \
    ln -s /opt/allure-2.20.1/bin/allure /usr/local/bin/allure && \
    rm allure-2.20.1.tgz

# Добавляем Allure CLI в PATH
ENV PATH="/opt/allure-2.20.1/bin:${PATH}"

# Добавляем том для отчётов
VOLUME ["/app/reports"]

# Проверяем версии браузеров и драйверов
RUN chromium --version && \
    chromedriver --version && \
    firefox --version && \
    geckodriver --version

# Делаем рабочую директорию доступной
WORKDIR /app

# Настраиваем возможность передачи параметров
ENTRYPOINT ["pytest"]
CMD ["--help"]