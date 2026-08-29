FROM python:3.13-slim

# Chrome + Firefox + Edge çalıştırmak için gerekli sistem kütüphaneleri
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    fonts-liberation libnss3 libatk-bridge2.0-0 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libpangocairo-1.0-0 libgtk-3-0 libdbus-glib-1-2 libxt6 libxtst6 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome kurulumu
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Mozilla Firefox kurulumu (Debian'da paket adı firefox-esr olarak gelir,
# Selenium/geckodriver'ın binary'yi bulabilmesi için 'firefox' symlink'i ekliyoruz)
RUN apt-get update && apt-get install -y firefox-esr --no-install-recommends \
    && ln -sf /usr/bin/firefox-esr /usr/bin/firefox \
    && rm -rf /var/lib/apt/lists/*

# Microsoft Edge kurulumu
RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-edge.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-edge.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update && apt-get install -y microsoft-edge-stable --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HEADLESS=true
ENV BROWSER=chrome
ENV PYTHONUNBUFFERED=1

CMD ["behave", "features/", "--tags=~@db", "--tags=~@mobile"]