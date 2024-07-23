# FROM node:18.8-alpine AS ReactImage
FROM node:22.0.0 AS ReactImage

WORKDIR /app/frontend

ENV NODE_PATH=/app/frontend/node_modules
ENV PATH=$PATH:/app/frontend/node_modules/.bin

# test that removing yarn works in this case
COPY ./frontend/package.json ./
RUN npm install --legacy-peer-deps

ADD ./frontend ./
RUN npm run build


FROM python:3.11-slim-buster AS ApiImage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip install poetry

# change to mount as volume => should we get the data here with an s3 command?
WORKDIR /app/
VOLUME [ "/data" ]
# COPY ./data/ ./data

RUN mkdir -p /app/backend
WORKDIR /app/backend

COPY ./backend/ .
# change to install with poetry
# RUN pip install -e . --no-cache-dir
RUN poetry install --no-dev

# add static react files to fastapi image
COPY --from=ReactImage /app/frontend/build /app/backend/arxivsearch/templates/build

LABEL org.opencontainers.image.source https://github.com/RedisVentures/redis-arxiv-search

# WORKDIR /app/backend/arxivsearch

CMD ["poetry", "run", "start-app"]
# CMD ["sh", "./entrypoint.sh"]