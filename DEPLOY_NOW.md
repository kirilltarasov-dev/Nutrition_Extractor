# 🚀 Развертывание СЕЙЧАС - Backend + Frontend на Railway

## ⚡ 3 шага до запуска

### 1️⃣ Backend (2 минуты)

1. Откройте https://railway.app
2. Нажмите "Start a New Project"
3. Выберите "Deploy from GitHub repo"
4. Выберите ваш репозиторий
5. **ГОТОВО!** Скопируйте URL (например: `https://nutrition-backend.up.railway.app`)

### 2️⃣ Frontend (2 минуты)

1. В Railway Dashboard нажмите **"+ New"**
2. Выберите "GitHub Repo" → тот же репозиторий
3. Откройте Settings сервиса:
   - Root Directory: `frontend`
   - Start Command: 
   ```bash
   npm install && npm run build && npx serve -s build -l $PORT
   ```
4. Settings → Variables:
   ```
   REACT_APP_API_URL=https://ваш-бэкенд-url.up.railway.app/api/v1
   ```
   ⚠️ Замените на реальный URL бэкенда из шага 1!

### 3️⃣ Готово!

Откройте Frontend URL и проверьте работу!

---

## 📋 Что сделано

✅ **Procfile** - команда запуска backend  
✅ **runtime.txt** - Python 3.11  
✅ **railway.json** - конфигурация Railway  
✅ **backend/requirements.txt** - зависимости  
✅ **frontend/nixpacks.toml** - конфигурация фронтенда  

---

## 🔧 Если что-то не работает

### Backend не запускается:
- Проверьте логи в Railway Dashboard
- Убедитесь, что Procfile в корне проекта

### Frontend не запускается:
- Проверьте Root Directory = `frontend`
- Проверьте Start Command
- Проверьте переменную `REACT_APP_API_URL`

### CORS ошибки:
- Добавьте в Backend Variables:
  ```
  BACKEND_CORS_ORIGINS=https://ваш-фронтенд-url.up.railway.app
  ```

---

## 📚 Подробная инструкция

Смотрите `RAILWAY_BOTH.md` для деталей.

