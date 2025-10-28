# Используем Node.js официальный образ
FROM node:18-alpine

# Установим рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем весь код
COPY . .

# Собираем приложение
RUN npm run build

# Устанавливаем serve
RUN npm install -g serve

# Запускаем сервер
CMD ["serve", "-s", "build", "-l", "3000"]

