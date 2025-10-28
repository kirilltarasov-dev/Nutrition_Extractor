# 🔍 Как найти запущенные сервисы на Railway

## 📍 Где находятся сервисы в интерфейсе

### В Railway Dashboard:

1. **Откройте проект**
   - Ссылка вида: https://railway.app/project/ваш-projekt-id
   - Или зайдите на railway.app → выберите ваш проект

2. **Список сервисов**
   - Внизу страницы вы увидите список сервисов
   - Каждый сервис - это отдельный контейнер
   - Их может быть 2: один для backend, один для frontend

3. **Как выглядит:**
```
┌─────────────────────────────────────┐
│  Nutrition Extractor Project        │
├─────────────────────────────────────┤
│                                     │
│  📦 Service 1 (Backend)             │
│  └─ [✓ Running] [📊 Metrics]      │
│                                     │
│  📦 Service 2 (Frontend)            │
│  └─ [✓ Running] [📊 Metrics]        │
│                                     │
└─────────────────────────────────────┘
```

---

## 🐛 Если не видите сервисы

### Проблема 1: Создали только один сервис

**Решение:**
1. Нажмите **"+ New"** в верхнем правом углу
2. Выберите **"GitHub Repo"**
3. Выберите тот же репозиторий
4. Это создаст второй сервис для фронтенда

### Проблема 2: Frontend не запускается

**Проверьте логи:**
1. Кликните на сервис
2. Перейдите на вкладку **"Logs"**
3. Смотрите на ошибки

**Частые проблемы:**

❌ **"npm install failed"**
```
Решение: Проверьте что Root Directory = frontend
```

❌ **"Cannot find module"**
```
Решение: Добавьте в Start Command: npm install && 
```

❌ **"Build failed"**
```
Решение: Проверьте Node.js версию в nixpacks.toml
```

---

## ⚙️ Правильная настройка Frontend сервиса

### Шаг 1: Создайте сервис

1. Нажмите "+ New"
2. Выберите "GitHub Repo"
3. Выберите ваш репозиторий

### Шаг 2: Настройте Deploy

1. Кликните на сервис
2. Settings → **Deploy**
3. Установите:
   - **Root Directory**: `frontend`
   - **Start Command**: 
   ```bash
   npm install && npm run build && npx serve -s build -l $PORT
   ```

### Шаг 3: Environment Variables

1. Settings → **Variables**
2. Добавьте:
   ```
   REACT_APP_API_URL=https://ваш-бэкенд-url.up.railway.app/api/v1
   PORT=3000
   ```

### Шаг 4: Redeploy

1. Settings → **Redeploy**
2. Или просто подождите авто-деплоя

---

## 🔍 Как проверить, что работает

### 1. Проверьте сервисы в Dashboard

```
Project Dashboard
├── 📦 backend-service
│   └── Status: [Running] 🟢
└── 📦 frontend-service
    └── Status: [Running] 🟢
```

### 2. Проверьте логи

**Backend лог должен показывать:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Frontend лог должен показывать:**
```
Serving!
  - Local:    http://localhost:3000
  - Listening on port 3000
```

### 3. Проверьте URLs

Каждый сервис имеет свой URL:
- Backend: `https://ваш-бэкенд.up.railway.app`
- Frontend: `https://ваш-фронтенд.up.railway.app`

Найдите URL в Settings → **Networking** каждого сервиса.

---

## 🎯 Быстрое решение проблем

### Если Frontend не видно вообще:

1. **Создайте сервис заново:**
   - "+ New" → "GitHub Repo"
   - Root: `frontend`
   - Start Command: `npm install && npm run build && npx serve -s build -l $PORT`

2. **Проверьте git:**
   ```bash
   git log --oneline -5
   # Убедитесь что последний коммит содержит изменения
   ```

3. **Принудительно перезапустите:**
   - Settings → Redeploy → Force Deploy

---

## 💡 Советы

✅ **Используйте разные имена для сервисов:**
   - Backend Service: "backend" или "api"
   - Frontend Service: "frontend" или "web"

✅ **Проверяйте логи регулярно:**
   - В Railway Dashboard → Logs
   - Красные строки = ошибки

✅ **Используйте Metrics:**
   - CPU, RAM usage
   - Network traffic

---

## 🆘 Если ничего не помогает

1. **Проверьте git status:**
   ```bash
   git status
   # Убедитесь что все изменения закоммичены
   ```

2. **Принудительный push:**
   ```bash
   git add .
   git commit -m "Fix deployment"
   git push --force
   ```

3. **Удалите сервис и создайте заново:**
   - Settings → Delete
   - Создайте заново с правильными настройками

