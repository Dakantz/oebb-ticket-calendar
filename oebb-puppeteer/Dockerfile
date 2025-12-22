FROM oven/bun:latest

COPY package.json ./
COPY src ./src
COPY tsconfig.json ./
RUN bun install



CMD ["bun", "run", "start"]