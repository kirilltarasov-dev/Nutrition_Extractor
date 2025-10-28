# 🚀 Полное развертывание Nutrition Extractor

Полная инструкция по развертыванию Backend + Frontend.

## 📋 Варианты развертывания

### Вариант 1: Vercel + Railway (Рекомендуется)

**Backend на Railway, Frontend на Vercel**

#### Backend (Railway):

1. Создайте проект на https://railway.app
2. Подключите GitHub репозиторий
3. Выберите корневую папку проекта
4. Railway автоматически определит Python 3.11
5. Получите URL: `https://your-backend.up.railway.app`

#### Frontend (Vercel):

1. Создайте проект на https://vercel.com
2. Подключите GitHub репозиторий
3. **Root Directory**: `frontend`
4. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app/api/v1
   ```
5. Нажмите Deploy
6. Получите URL: `https://your-app.vercel.app`

**✅ Преимущества**:
- Бесплатный план для обоих сервисов
- Автоматические деплои при push
- Отличная производительность
- Разделение ответственности

---

### Вариант 2: Railway (Backend + Frontend)

**Все на Railway (2 сервиса)**

#### Backend Service:

1. Создайте проект на Railway
2. Подключите репозиторий
3. Получите URL: `https://backend.up.railway.app`

#### Frontend Service:

1. В том же проекте нажмите "+ New"
2. Подключите тот же репозиторий
3. **Settings → Deploy**:
   - Root Directory: `frontend`
   - Start Command: `cd frontend && npm install && npm run build && npx serve -s build -l $PORT`
4. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://backend.up.railway.app/api/v1
   PORT=3000
   ```
5. Получите URL: `https://frontend.up.railway.app`

**✅ Преимущества**:
- Все в одном месте
- Единый биллинг
- Простое управление

---

### Вариант 3: Vercel (Unified Deploy)

**Все на Vercel (Backend + Frontend вместе)**

Это требует более сложной настройки. Смотрите `vercel.json` в корне.

⚠️ **Не рекомендуется** для этого проекта, так как backend использует специальные библиотеки.

---

## 🔧 Пошаговая инструкция

### Шаг 1: Подготовка Backend на Railway

```bash
# 1. Закоммитьте изменения
git add .
git commit -m "Add Railway configuration"
git push

# 2. Создайте проект на Railway
# - Откройте railway.app
# - Start a New Project
# - Deploy from GitHub repo
# - Выберите ваш репозиторий

# 3. Дождитесь деплоя (2-3 минуты)
# 4. Скопируйте URL (например: https://nutrition-backend.up.railway.app)
```

### Шаг 2: Подготовка Frontend на Vercel

```bash
# 1. Создайте проект на Vercel
# - Откройте vercel.com
# - Import Project
# - Выберите ваш репозиторий

# 2. Настройте:
# - Framework: Create React App
# - Root Directory: frontend
# - Build Command: npm run build
# - Output Directory: build
# - Install Command: npm install

# 3. Environment Variables:
# - REACT_APP_API_URL = https://nutrition-backend.up.railway.app/api/v1

# 4. Deploy
# 5. Скопируйте URL (например: https://nutrition-app.vercel.app)
```

### Шаг 3: Настройка CORS (если нужно)

Если после деплоя видите CORS ошибки:

1. Откройте Railway Dashboard
2. Перейдите в Backend сервис
3. Settings → Variables
4. Добавьте:
   ```
   BACKEND_CORS_ORIGINS=https://nutrition-app.vercel.app,https://nutrition-app.vercel.app/*
   ```

Или обновите `backend/app/core/config.py`:

```python
BACKEND_CORS_ORIGINS: List[str] = [
    "https://nutrition-app.vercel.app",
    "https://your-custom-domain.com"
]
```

---

## ✅ Проверка работоспособности

### Backend:

```bash
# Health check
curl https://your-backend.up.railway.app/health

# API Docs
open https://your-backend.up.railway.app/docs

# Root endpoint
curl https://your-backend.up.railway.app/
```

### Frontend:

```bash
# Откройте в браузере
open https://your-app.vercel.app

# Проверьте в DevTools → Console
# Должно быть без ошибок

# Попробуйте загрузить PDF
# - Введите API key
# - Выберите файл
# - Нажмите Extract
```

---

## 🔄 Обновление

### Автоматическое:

Оба сервиса автоматически перезапускаются при push в main ветку:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway и Vercel автоматически запустят новый деплой.

### Ручное:

**Railway:**
```bash
railway up
```

**Vercel:**
- Откройте Dashboard
- Нажмите "Redeploy"

---

## 💰 Стоимость

### Hobby Plan (Бесплатно):
- ✅ Railway: $5 бесплатных кредитов
- ✅ Vercel: Бесплатно для статики
- ⚠️ Лимиты: 100 часов/месяц на Railway

### Production:
- Railway Pro: $20/месяц
- Vercel Pro: $20/месяц
- Итого: ~$40/месяц

---

## 📚 Дополнительная документация

- **Backend**: `RAILWAY_DEPLOY.md` или `RAILWAY_QUICK_START.md`
- **Frontend**: `FRONTEND_DEPLOY.md`
- **Общая**: `README.md`

---

## 🆘 Troubleshooting

### Backend не запускается

**Проблема**: "ModuleNotFoundError"  
**Решение**: Убедитесь, что `requirements.txt` в папке `backend/`

**Проблема**: "Port binding failed"  
**Решение**: Используйте переменную `$PORT` (уже настроено в Procfile)

**Проблема**: "Memory exceeded"  
**Решение**: Увеличьте RAM в Railway Settings

### Frontend не подключается к Backend

**Проблема**: Network Error  
**Решение**: 
1. Проверьте `REACT_APP_API_URL` в Vercel
2. Проверьте, что backend работает
3. Проверьте CORS настройки

**Проблема**: CORS Error  
**Решение**: 
1. Обновите `BACKEND_CORS_ORIGINS` в Railway
2. Добавьте URL фронтенда в список

### Build Failed

**Проблема**: npm install failed  
**Решение**: 
1. Проверьте `package.json` в `frontend/`
2. Попробуйте `npm install` локально
3. Проверьте версию Node.js

---

## 🎉 Готово!

После развертывания ваш Nutrition Extractor будет доступен на вашем URL!

**Next steps**:
1. Настройте custom domain (опционально)
2. Добавьте мониторинг (опционально)
3. Настройте автоматические бэкапы (опционально)

