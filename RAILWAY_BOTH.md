# 🚂 Развертывание Backend + Frontend на Railway

Пошаговая инструкция для развертывания обоих сервисов на Railway.

## 📋 Предварительные требования

- Аккаунт на Railway: https://railway.app
- Код в Git репозитории (GitHub/GitLab/Bitbucket)
- API ключ Google Gemini (будет вводиться пользователем)

## 🎯 Вариант 1: 2 отдельных сервиса (Рекомендуется)

### Шаг 1: Backend на Railway

1. **Создайте проект**
   - Откройте https://railway.app
   - Нажмите "Start a New Project"
   - Выберите "Deploy from GitHub repo"

2. **Выберите репозиторий**
   - Найдите ваш репозиторий
   - Выберите его
   - Railway автоматически определит это как Python приложение

3. **Проверьте настройки**
   - Root Directory: `/` (по умолчанию)
   - Railway автоматически использует:
     - `Procfile` для запуска
     - `runtime.txt` для Python версии
     - `backend/requirements.txt` для зависимостей

4. **Деплой**
   - Дождитесь завершения (2-3 минуты)
   - Получите URL: `https://your-backend-name.up.railway.app`
   - **Скопируйте этот URL**

5. **Переменные окружения** (опционально)
   - Settings → Variables
   - Добавьте если нужно:
     ```
     PYTHONPATH=/app/backend
     LOG_LEVEL=INFO
     ```

### Шаг 2: Frontend на Railway

1. **Создайте второй сервис**
   - В том же проекте нажмите **"+ New"**
   - Выберите **"GitHub Repo"**
   - **Выберите тот же репозиторий**

2. **Настройте Frontend сервис**
   - Railway Settings → Deploy
   - Root Directory: `frontend`
   
3. **Custom Start Command**
   - Settings → Deploy → Custom Start Command
   - Вставьте:
   ```bash
   npm install && npm run build && npx serve -s build -l $PORT
   ```

4. **Переменные окружения**
   - Settings → Variables
   - Добавьте:
   ```
   REACT_APP_API_URL=https://your-backend-name.up.railway.app/api/v1
   PORT=3000
   ```

5. **Деплой**
   - Дождитесь завершения
   - Получите URL: `https://your-frontend-name.up.railway.app`

---

## 🎯 Вариант 2: Простой (для начала)

Если хотите быстрее:

### Backend:

```bash
# 1. Откройте railway.app
# 2. New Project → Deploy from GitHub
# 3. Выберите репозиторий
# 4. Дождитесь деплоя
# 5. Скопируйте URL бэкенда
```

### Frontend:

```bash
# 1. В том же проекте: + New
# 2. Deploy from GitHub (тот же репозиторий)
# 3. Settings → Root Directory: frontend
# 4. Settings → Start Command:
#    npm install && npm run build && npx serve -s build -l $PORT
# 5. Settings → Variables:
#    REACT_APP_API_URL=https://ваш-бэкенд.up.railway.app/api/v1
# 6. Деплой
```

---

## 📝 Структура на Railway

```
Railway Project
├── Backend Service
│   ├── Root: / (project root)
│   ├── Start: Procfile (cd backend && uvicorn app.main:app...)
│   └── URL: backend-name.up.railway.app
└── Frontend Service  
    ├── Root: frontend/
    ├── Start: npm install && npm run build && npx serve...
    └── URL: frontend-name.up.railway.app
```

---

## ⚙️ Настройка CORS

После деплоя, если видите CORS ошибки:

### Способ 1: Через Railway Variables

1. Откройте Backend Service
2. Settings → Variables
3. Добавьте:
   ```
   BACKEND_CORS_ORIGINS=https://frontend-name.up.railway.app
   ```

### Способ 2: Обновить config.py

Отредактируйте `backend/app/core/config.py`:

```python
BACKEND_CORS_ORIGINS: List[str] = [
    "https://your-frontend-name.up.railway.app",
    "https://your-frontend-name.up.railway.app/*"
]
```

Затем запушите изменения:
```bash
git add backend/app/core/config.py
git commit -m "Update CORS settings"
git push
```

---

## ✅ Проверка работоспособности

### 1. Проверка Backend

```bash
# Health check
curl https://your-backend.up.railway.app/health

# Должен вернуть:
# {"status":"healthy","version":"1.0.0"}

# API Docs
# Откройте в браузере:
https://your-backend.up.railway.app/docs
```

### 2. Проверка Frontend

```bash
# Откройте в браузере:
https://your-frontend.up.railway.app

# Должна загрузиться страница приложения
# Проверьте консоль браузера (F12) - не должно быть ошибок
```

### 3. Проверка соединения

1. Откройте Frontend URL
2. Введите API key (Google Gemini)
3. Загрузите тестовый PDF
4. Нажмите "Extract Data"
5. Проверьте, что данные извлекаются

---

## 🔄 Обновление кода

После каждого push в main ветку:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway автоматически:
1. Определит изменения
2. Перезапустит сервисы с новым кодом
3. Задеплоит новую версию

---

## 🐛 Troubleshooting

### Backend не запускается

**Проблема**: "ModuleNotFoundError"  
**Решение**: 
- Проверьте, что `backend/requirements.txt` существует
- Проверьте, что Root Directory не указан (или указан как `/`)

**Проблема**: "Port binding failed"  
**Решение**: 
- Проверьте, что Procfile использует `$PORT`
- Уже настроено в Procfile

**Проблема**: Build timeout  
**Решение**: 
- Увеличьте ресурсы в Settings → Resources
- Минимум: 512MB RAM

### Frontend не запускается

**Проблема**: "npm install failed"  
**Решение**: 
- Проверьте, что Root Directory = `frontend`
- Проверьте `frontend/package.json`

**Проблема**: "Build failed"  
**Решение**: 
- Проверьте логи в Railway Dashboard
- Убедитесь, что Node.js версия поддерживается
- Попробуйте локально: `cd frontend && npm run build`

**Проблема**: "Cannot find module"  
**Решение**: 
- Добавьте `npm install` в Start Command
- Или используйте: `npm ci && npm run build && npx serve...`

### Frontend не подключается к Backend

**Проблема**: Network Error  
**Решение**: 
1. Проверьте `REACT_APP_API_URL` в Frontend variables
2. Проверьте, что backend запущен и работает
3. Проверьте CORS настройки

**Проблема**: CORS Error  
**Решение**: 
1. Добавьте URL фронтенда в `BACKEND_CORS_ORIGINS`
2. Перезапустите backend

---

## 💰 Стоимость

### Hobby Plan (Бесплатно):
- $5 бесплатных кредитов каждый месяц
- Достаточно для Backend + Frontend
- Примерно 100 часов работы в месяц

### Pro Plan ($20/месяц):
- Если нужны дополнительные ресурсы
- Больше RAM и CPU
- Приоритетная поддержка

---

## 📊 Мониторинг

### Логи

Просмотр логов в реальном времени:
1. Откройте сервис в Railway Dashboard
2. Нажмите "View Logs"
3. Видите live логи

### Метрики

Просмотр использования ресурсов:
1. Settings → Resources
2. Видите CPU, RAM, Network

---

## 🎯 Quick Deploy Checklist

- [ ] Создан аккаунт на Railway
- [ ] Backend развернут на Railway
- [ ] URL бэкенда скопирован
- [ ] Frontend развернут на Railway
- [ ] `REACT_APP_API_URL` установлен в Frontend variables
- [ ] CORS настроен на Backend
- [ ] Health check работает
- [ ] Frontend загружается
- [ ] Тестовая загрузка PDF работает
- [ ] Все работает! 🎉

---

## 📞 Дополнительная помощь

- **Railway Docs**: https://docs.railway.app
- **Discord**: https://discord.gg/railway
- **Примеры**: https://railway.app/templates

