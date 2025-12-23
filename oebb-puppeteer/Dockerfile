FROM oven/bun:latest

RUN apt-get update && apt-get install -y \
    chromium \
    fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-freefont-ttf \
    ca-certificates \
    wget \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Puppeteer
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    NODE_ENV=production

WORKDIR /app
ARG USERNAME=oebb-puppeteer
ARG USER_UID=1005
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && chown -R $USERNAME:$USERNAME /app

RUN mkdir data
RUN chown -R $USERNAME:$USERNAME /app/data
USER $USERNAME

COPY package.json ./
COPY tsconfig.json ./
RUN bun install
COPY src ./src
EXPOSE 3000


CMD ["bun", "run", "start"]