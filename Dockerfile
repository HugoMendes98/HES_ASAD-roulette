FROM node:20-alpine as node

WORKDIR /app
COPY frontend .

RUN npm ci
RUN npm run build

FROM python:3.11

WORKDIR /app
COPY backend .

RUN pip install -r requirements.txt

COPY --from=node /app/dist/frontend/browser ./src/static

ENV APP_HOST="0.0.0.0"
ENV APP_POST="5000"

CMD ["python3", "/app/main.py"]
