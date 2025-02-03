# Используем минимальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    default-jre \
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

# Устанавливаем Chrome и ChromeDriver
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

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

# Копируем весь проект
COPY . /app

# Устанавливаем Allure
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.tgz && \
    tar -xzf allure-2.20.1.tgz -C /opt/ && \
    ln -s /opt/allure-2.20.1/bin/allure /usr/local/bin/allure && \
    rm allure-2.20.1.tgz

# Добавляем Allure CLI в PATH
ENV PATH="/opt/allure-2.20.1/bin:${PATH}"

# Добавляем том для отчетов
VOLUME ["/app/reports"]

# Проверяем версии браузеров и драйверов
RUN google-chrome --version && \
    chromedriver --version && \
    geckodriver --version

# Копируем скрипт ожидания
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Запускаем тесты после ожидания OpenCart
CMD ["./wait-for-it.sh", "opencart", "8080", "--", "pytest", "tests", "--browser", "chrome", "--browser-version", "114.0", "--alluredir=/app/reports"]