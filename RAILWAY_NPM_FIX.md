# 🔧 ИСПРАВЛЕНИЕ: npm: command not found

## Проблема:

Railway пытается запустить Node.js команды в Python контейнере.

## ✅ Решение:

**Удалите Start Command из Procfile** и установите его прямо в Railway!

---

## 📝 Что делать:

### В Railway Dashboard для Frontend сервиса:

**Settings → Deploy:**

1. **Удалите** или **оставьте пустым** поле Start Command

2. **Root Directory:** `frontend` ⚠️ КРИТИЧНО!

3. **Railway автоматически:**
   - Определит Node.js из package.json
   - Установит Node.js 18.x
   - Выполнит npm install
   - Запустит npm run build
   - Запустит npx serve

---

## 🔧 Альтернативное решение:

Если автоматическое определение не работает:

**Settings → Deploy → Start Command:**
```bash
cd frontend && npm install && npm run build && npx serve -s build -l $PORT
```

---

## ⚠️ Важно:

Убедитесь что в корне НЕТ Procfile для frontend!

Корневой Procfile используется только для backend!

Для frontend используйте:
- Root Directory: `frontend`
- Или прямое указание Start Command

