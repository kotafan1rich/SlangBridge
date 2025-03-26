#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Пожалуйста, установите его."
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "Устанавливаем зависимости из requirements.txt..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
else
    echo "Файл requirements.txt не найден. Продолжаем без установки зависимостей."
fi

if [ -f "src/main.py" ]; then
    echo "Запускаем main.py..."
    cd src
    python main.py
else
    echo "Файл main.py не найден. Пожалуйста, убедитесь, что он существует."
    exit 1
fi
