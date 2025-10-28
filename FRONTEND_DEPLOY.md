# Развертывание Frontend

Frontend можно развернуть несколькими способами. Выберите наиболее подходящий для вас.

## 🎯 Варианты развертывания

### 1. Vercel (Рекомендуется - Проще всего)

Frontend уже настроен для Vercel с конфигурацией в `frontend/vercel.json`.

#### Шаги:

1. **Подключите GitHub репозиторий**
   - Зайдите на https://vercel.com
   - Нажмите "Import Project"
   - Выберите ваш репозиторий

2. **Настройте проект**
   - Root Directory: `frontend`
   - Framework: Create React App (определится автоматически)
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

3. **Переменные окружения** (если нужно)
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app/api/v1
   ```

4. **Деплой**
   - Нажмите "Deploy"
   - Готово! Vercel даст вам URL

#### Преимущества Vercel:
- ✅ Бесплатный план для статики
- ✅ Автоматический HTTPS
- ✅ CDN по всему миру
- ✅ Автоматические деплои при push

---

### 2. Railway (Отдельный Frontend сервис)

Если хотите развернуть фронтенд на Railway рядом с бэкендом.

#### Шаги:

1. **Создайте новый сервис в Railway**
   - В существующем проекте нажмите "+ New"
   - Выберите "GitHub Repo"
   - Выберите тот же репозиторий

2. **Настройте сервис**
   - Root Directory: `frontend`
   - Start Command: `npm start` (для разработки) или создайте custom
   
3. **Создайте `railway.json` для фронтенда**:
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

4. **Переменные окружения**:
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app/api/v1
   PORT=3000
   ```

5. **Custom Start Command в Railway**
   - Settings → Deploy
   - Start Command: `cd frontend && npm install && npm run build && npx serve -s build -l $PORT`

---

### 3. Netlify

Альтернатива Vercel.

#### Шаги:

1. Зайдите на https://netlify.com
2. Подключите GitHub
3. Build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
4. Environment variables:
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app/api/v1
   ```

---

### 4. Объединенный деплой на Railway (Backend + Frontend вместе)

Для этого нужно создать Docker-based деплой или использовать nginx.

#### Создайте `Dockerfile` в корне проекта:

```dockerfile
# Backend
FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js for frontend
RUN apt-get update && apt-get install -y nodejs npm

# Build frontend
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

# Copy backend code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Start backend (frontend будет served статически)
CMD ["cd", "backend", "&&", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Но это требует более сложной настройки. Лучше использовать варианты 1 или 2.

---

## 🔗 Подключение Frontend к Backend

После развертывания обоих сервисов нужно:

### Вариант A: Обновить CORS на Backend

В `backend/app/main.py` уже настроен CORS:
```python
BACKEND_CORS_ORIGINS: List[str] = ["*"]
```

Если хотите ограничить:
```python
BACKEND_CORS_ORIGINS: List[str] = [
    "https://your-frontend.vercel.app",
    "https://your-frontend.up.railway.app"
]
```

### Вариант B: Использовать переменную окружения на Frontend

При деплое фронтенда установите переменную:
```
REACT_APP_API_URL=https://your-backend.up.railway.app/api/v1
```

---

## 📊 Рекомендуемая конфигурация

### Для Production:

**Backend**: Railway  
**Frontend**: Vercel  
**Причина**: 
- Vercel бесплатен для статики
- Railway хорош для backend
- Разделение ответственности

### Альтернатива:

**Backend**: Railway  
**Frontend**: Railway (отдельный сервис)  
**Причина**: 
- Все в одном месте
- Проще управлять
- Но дороже (оба потребляют RAM)

---

## 🔍 Проверка после деплоя

1. **Frontend работает**:
   ```
   https://your-frontend.vercel.app
   ```

2. **Подключение к Backend**:
   - Введите API key на фронтенде
   - Попробуйте загрузить PDF
   - Проверьте в DevTools → Network, что запросы идут на правильный backend

3. **CORS ошибки**:
   - Проверьте настройки CORS в backend
   - Убедитесь, что `BACKEND_CORS_ORIGINS` содержит URL фронтенда

---

## 🐛 Troubleshooting

### "Network Error" при отправке запроса

**Причина**: Frontend не может подключиться к Backend

**Решение**:
1. Проверьте `REACT_APP_API_URL` в переменных окружения
2. Проверьте, что backend запущен
3. Проверьте CORS настройки на backend

### "CORS policy: No 'Access-Control-Allow-Origin'"

**Причина**: Backend не разрешает запросы с вашего фронтенда

**Решение**:
1. Обновите `BACKEND_CORS_ORIGINS` в backend settings
2. Добавьте URL вашего фронтенда

### Frontend показывает пустую страницу

**Причина**: Ошибка сборки или отсутствие переменных

**Решение**:
1. Проверьте логи деплоя
2. Проверьте консоль браузера (F12)
3. Убедитесь, что все env переменные установлены

---

## 📚 Полезные ссылки

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [React App Deploy](https://create-react-app.dev/docs/deployment/)

