FROM node:22-bookworm-slim

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV NEXT_TELEMETRY_DISABLED=1

EXPOSE 3000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
