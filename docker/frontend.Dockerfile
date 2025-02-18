FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY client/package.json client/package-lock.json* ./
RUN npm ci

# Copy application code
COPY client/src ./src
COPY client/public ./public
COPY client/index.html client/vite.config.ts client/tsconfig.json ./

# Build the application
RUN npm run build

# Expose port
EXPOSE 5173

# Start the application
CMD ["npm", "run", "dev", "--", "--host"]