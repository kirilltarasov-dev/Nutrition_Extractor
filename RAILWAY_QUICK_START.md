# 🚀 Быстрое развертывание на Railway

## Шаги развертывания

### 1. Подготовка (5 минут)

1. Создайте аккаунт на [Railway.app](https://railway.app)
2. Убедитесь, что ваш код в Git (GitHub/GitLab/Bitbucket)

### 2. Деплой через веб-интерфейс

1. **Войдите** на https://railway.app
2. Нажмите **"Start a New Project"**
3. Выберите **"Deploy from GitHub repo"**
4. Выберите ваш репозиторий
5. **Готово!** Railway автоматически:
   - Найдет Python 3.11
   - Установит зависимости из `backend/requirements.txt`
   - Запустит сервер на порту из переменной $PORT

### 3. Получите URL

После деплоя Railway даст вам URL вида:
```
https://your-app-name.up.railway.app
```

## 📝 Проверка работоспособности

1. **Health Check**
   ```
   https://your-app.up.railway.app/health
   ```

2. **API Documentation**
   ```
   https://your-app.up.railway.app/docs
   ```

## ⚙️ Переменные окружения (опционально)

В Railway Dashboard → Settings → Variables добавьте:

```
PYTHONPATH=/app/backend
OPENAI_API_KEY=sk-... (если нужно)
LOG_LEVEL=INFO
```

## 📦 Что уже настроено

✅ **Procfile** - команда запуска  
✅ **runtime.txt** - Python 3.11  
✅ **requirements.txt** - зависимости  
✅ **railway.json** - конфигурация  

## 🔄 Обновление

После каждого push в main ветку Railway автоматически задеплоит новую версию.

## 💰 Стоимость

- **Hobby Plan**: $5 бесплатных кредитов каждый месяц
- **Pro Plan**: $20/месяц для серьезных проектов

## 🆘 Проблемы?

- Проверьте логи в Railway Dashboard
- Убедитесь, что файлы на месте:
  - Procfile
  - runtime.txt
  - backend/requirements.txt
  - backend/app/main.py

## 📚 Подробная инструкция

Смотрите `RAILWAY_DEPLOY.md` для детальной информации.

