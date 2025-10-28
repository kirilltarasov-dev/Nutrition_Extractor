# 🔧 Исправление: Frontend не видно в Railway

## 🎯 Вероятная причина

Вы создали только **один сервис** (backend), но фронтенд требует **отдельный сервис**.

---

## ✅ Быстрое решение (5 минут)

### Шаг 1: Создайте Frontend сервис

1. **Откройте ваш проект в Railway:**
   ```
   https://railway.app/project/your-project-id
   ```

2. **Нажмите "+ New"** (в правом верхнем углу или внизу списка сервисов)

3. **Выберите "GitHub Repo"**

4. **Выберите ваш репозиторий** (тот же самый)

### Шаг 2: Настройте Frontend

После создания сервиса:

1. **Кликните на новый сервис**

2. **Settings → Deploy:**
   - Root Directory: `frontend`
   - Custom Start Command:
   ```bash
   npm install && npm run build && npx serve -s build -l $PORT
   ```

3. **Settings → Variables:**
   ```
   REACT_APP_API_URL=https://ваш-бэкенд-url.up.railway.app/api/v1
   ```
   ⚠️ Замените на реальный URL вашего backend!

4. **Settings → Resources:**
   - Или оставьте по умолчанию
   - Или увеличьте RAM до 512MB

### Шаг 3: Сохраните и дождитесь деплоя

Railway автоматически перезапустит сервис с новыми настройками.

---

## 📍 Где найти запущенные сервисы

### В Dashboard:

```
Project: Nutrition Extractor
├── 📦 nutrition-backend-xxxxx
│   ├── Status: Running 🟢
│   ├── URL: https://nutrition-backend.up.railway.app
│   └── [Settings] [Logs] [Metrics]
│
└── 📦 nutrition-frontend-xxxxx
    ├── Status: Running 🟢
    ├── URL: https://nutrition-frontend.up.railway.app
    └── [Settings] [Logs] [Metrics]
```

**Каждый сервис - это отдельная карточка!**

### Если видите только один сервис:

→ Создайте второй по инструкции выше

---

## 🔍 Как проверить, что Frontend работает

### 1. Откройте Logs

Кликните на сервис → вкладка **"Logs"**

Должно быть что-то вроде:
```
Preparing build...
Installing dependencies...
Building...
Generating static HTML...
Listening on port 3000
```

### 2. Откройте URL

Найдите URL в **Settings → Networking**

Откройте в браузере - должна загрузиться страница приложения.

### 3. Проверьте переменные

Settings → Variables:
```
✓ REACT_APP_API_URL = https://backend.up.railway.app/api/v1
```

---

## 🐛 Частые ошибки и решения

### Ошибка 1: "Cannot find module 'serve'"

**Причина:** Отсутствует пакет `serve`  
**Решение:** Добавьте в Start Command:
```bash
npm install -g serve && npm install && npm run build && serve -s build -l $PORT
```

Или используйте:
```bash
npm install && npm run build && npx serve -s build -l $PORT
```

### Ошибка 2: "Build failed"

**Причина:** Node.js версия  
**Решение:** Проверьте в логах версию Node.js. Если старая, добавьте в Root:
```
node-version: 18.x
```

### Ошибка 3: "ENOENT: no such file or directory"

**Причина:** Root Directory неправильный  
**Решение:** Убедитесь что Root Directory = `frontend` (не `/frontend`)

---

## 🎯 Пошаговый чеклист

- [ ] Создали второй сервис в Railway
- [ ] Root Directory = `frontend`
- [ ] Start Command добавлен
- [ ] `REACT_APP_API_URL` установлен с URL backend
- [ ] Сервис запустился без ошибок
- [ ] Logs показывают "Listening on port..."
- [ ] URL работает в браузере

---

## 💡 Альтернативное решение: Через Nixpacks

Если проблема с npm командами, используйте `frontend/nixpacks.toml`:

1. Railway автоматически определит Nixpacks
2. Использует конфигурацию из `nixpacks.toml`
3. Но нужно убедиться что файл в репозитории:

```bash
git add frontend/nixpacks.toml
git commit -m "Add nixpacks config"
git push
```

Затем перезапустите сервис.

---

## 📞 Если все еще не работает

Проверьте:
1. Все файлы закоммичены: `git status`
2. Пуш на GitHub выполнен: `git log`
3. Railway подключен к правильному репозиторию
4. Последний коммит в Railway: Settings → Source

