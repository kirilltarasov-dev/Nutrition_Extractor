# Railway Deployment Guide

Пошаговая инструкция по развертыванию Nutrition Extractor на Railway.

## 📋 Подготовка

### 1. Требования
- Аккаунт на [Railway](https://railway.app)
- Код в Git-репозитории (GitHub, GitLab, или Bitbucket)
- API ключ Google Gemini (опционально, если хотите предустановить)

### 2. Файлы конфигурации

Проект уже содержит все необходимые файлы:
- ✅ `Procfile` - команда запуска
- ✅ `runtime.txt` - версия Python (3.11)
- ✅ `requirements.txt` - зависимости
- ✅ `railway.json` - конфигурация Railway

## 🚀 Развертывание на Railway

### Вариант 1: Через Railway CLI

```bash
# Установите Railway CLI
npm i -g @railway/cli

# Войдите в аккаунт
railway login

# Создайте новый проект
railway init

# Подключите к существующему проекту (если есть)
railway link

# Разверните
railway up
```

### Вариант 2: Через Railway Dashboard (Рекомендуется)

1. **Войдите в Railway**
   - Откройте https://railway.app
   - Нажмите "Start a New Project"

2. **Подключите репозиторий**
   - Выберите "Deploy from GitHub repo"
   - Выберите ваш репозиторий
   - Railway автоматически определит Python приложение

3. **Проверьте настройки**
   - Railway автоматически найдет `backend/requirements.txt`
   - Установит Python 3.11 из `runtime.txt`
   - Запустит команду из `Procfile`

4. **Переменные окружения** (если нужно)
   ```
   PYTHONPATH=/app/backend
   PORT=8000
   ```

5. **Деплой**
   - Railway автоматически начнет деплой
   - Дождитесь завершения (2-3 минуты)
   - Получите публичный URL

## ⚙️ Конфигурация

### Переменные окружения

В Railway Dashboard → Variables можно добавить:

```
OPENAI_API_KEY=your_key_here (необязательно)
GEMINI_API_KEY=your_key_here (необязательно)
PYTHONPATH=/app/backend
LOG_LEVEL=INFO
```

### Выбор порта

Railway автоматически предоставляет переменную `$PORT`. 
Приложение уже настроено для использования переменной PORT из окружения.

### Масштабирование

В Railway Dashboard → Settings → Resources:
- Выберите план (Hobby, Pro, etc.)
- Настройте RAM (минимум 512MB рекомендуется)

## 📝 Структура проекта

Railway будет использовать следующие файлы:

```
nutrition-extractor/
├── Procfile              # ← Команда запуска для Railway
├── runtime.txt           # ← Версия Python
├── railway.json          # ← Конфигурация Railway
├── backend/
│   ├── requirements.txt  # ← Зависимости Python
│   └── app/
│       └── main.py       # ← Точка входа приложения
└── README.md
```

## 🔍 Проверка развертывания

После деплоя:

1. **Health Check**
   ```
   https://your-app.railway.app/health
   ```

2. **API Docs**
   ```
   https://your-app.railway.app/docs
   ```

3. **Root Endpoint**
   ```
   https://your-app.railway.app/
   ```

## 🐛 Troubleshooting

### Проблема: "ModuleNotFoundError"
**Решение:** Убедитесь, что `PYTHONPATH=/app/backend` установлен

### Проблема: "Port binding failed"
**Решение:** Используйте переменную `$PORT` (уже настроено в Procfile)

### Проблема: "Memory exceeded"
**Решение:** Увеличьте RAM в настройках Railway

### Проблема: "Build failed"
**Решение:** 
- Проверьте `requirements.txt` на ошибки
- Убедитесь, что `runtime.txt` содержит правильную версию
- Проверьте логи в Railway Dashboard

## 🔄 Обновление

После каждого push в main ветку Railway автоматически пересоберет и задеплоит приложение.

Для ручного деплоя:
```bash
railway up
```

## 💰 Стоимость

- **Hobby Plan**: Бесплатно с ограничениями
  - 100 часов в месяц
  - 512MB RAM
  - 1GB Storage
  
- **Pro Plan**: $5/месяц
  - $0.15 за использованные 100 часов
  - 1GB RAM
  - 5GB Storage

## 📚 Дополнительные ресурсы

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Project README](./README.md)

## ⚡ Быстрый старт

1. Создайте проект на Railway
2. Подключите GitHub репозиторий
3. Дождитесь автоматического деплоя
4. Откройте полученный URL
5. Готово! 🎉

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи в Railway Dashboard
2. Посмотрите [README.md](./README.md)
3. Откройте issue в репозитории

