FROM node:18.8-alpine AS ReactImage

WORKDIR /app/frontend

ENV NODE_PATH=/app/frontend/node_modules
ENV PATH=$PATH:/app/frontend/node_modules/.bin

COPY ./frontend/package.json ./
RUN yarn install --no-optional

ADD ./frontend ./
RUN yarn build


FROM python:3.9-slim-buster AS ApiImage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python3 -m pip install --upgrade pip setuptools wheel

WORKDIR /app/
COPY ./data/ ./data

RUN mkdir -p /app/backend
WORKDIR /app/backend

COPY ./backend/ .
RUN pip install -e . --no-cache-dir

# add static react files to fastapi image
COPY --from=ReactImage /app/frontend/build /app/backend/arxivsearch/templates/build

LABEL org.opencontainers.image.source https://github.com/RedisVentures/redis-arxiv-search

WORKDIR /app/backend/arxivsearch

CMD ["sh", "./entrypoint.sh"]