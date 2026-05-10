# ── Stage 1: Build Angular (browser only, no SSR) ────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build browser bundle only (faster, no SSR needed for Docker/nginx)
RUN npx ng build --configuration production \
    --output-path=dist/ecommerce-frontend \
    2>&1 | tail -20

# ── Stage 2: Serve with Nginx ─────────────────────────────────────────────────
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy browser build output
COPY --from=builder /app/dist/ecommerce-frontend/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
