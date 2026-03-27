FROM node:22-bookworm-slim

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9.15.4 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV NEXT_TELEMETRY_DISABLED=1

EXPOSE 3000

ENTRYPOINT ["/docker-entrypoint.sh"]
# pnpm run dev -- … だと「--」が next に渡り /app/--hostname 扱いになるため、直接 next を起動する
CMD ["pnpm", "exec", "next", "dev", "--turbopack", "--hostname", "0.0.0.0", "--port", "3000"]
