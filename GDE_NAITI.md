# 🔍 ГДЕ НАЙТИ ФРОНТЕНД В RAILWAY

## ⚡ Быстрый ответ:

**Фронтенд - это ОТДЕЛЬНЫЙ сервис!**

Если вы видите только 1 сервис (backend), вам нужно:
1. Создать ВТОРОЙ сервис для фронтенда
2. Настроить его правильно

---

## 📍 Где находятся сервисы:

```
Railway Dashboard
└── Your Project
    ├── Service 1: backend ✅
    └── Service 2: frontend ❌ (нужно создать!)
```

**Каждый сервис = отдельная карточка внизу экрана**

---

## ✅ Создание Frontend сервиса (3 клика):

1. **Нажмите "+ New"** (кнопка вверху или внизу)
2. **"GitHub Repo"** → выберите ваш репозиторий
3. **Новый сервис создан!**

Теперь настройте его:

### Настройки:
- Settings → Root Directory: `frontend`
- Settings → Start Command: 
  ```bash
  npm install && npm run build && npx serve -s build -l $PORT
  ```
- Settings → Variables → Add:
  ```
  REACT_APP_API_URL=https://backend-url.up.railway.app/api/v1
  ```

---

## 🎯 Как понять, что это Frontend:

**В списке сервисов увидите:**
- 🟢 **backend** - первый сервис (Python/Backend)
- 🟢 **frontend** - второй сервис (Node.js/Frontend)

**Если видите только один** → создайте второй!

---

## 💡 Если не можете найти:

1. Откройте: https://railway.app
2. Выберите ваш проект
3. Прокрутите вниз - увидите список сервисов
4. Если только 1 сервис → нажмите "+ New"

