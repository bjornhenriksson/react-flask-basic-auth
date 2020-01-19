
FROM node:12.2.0-alpine as client
COPY . .
ENV PATH node_modules/.bin:$PATH
RUN npm ci
RUN npm run build

FROM python:3.7-alpine as server
COPY --from=client . .
ENV FLASK_APP "app:main"
ENV FLASK_RUN_HOST "0.0.0.0"
ENV FLASK_ENV "development"
RUN pip install -r requirements.txt

FROM server as dev
CMD ["flask", "run"]

FROM server as prod
CMD ["waitress-serve", "--call", "app:main"]
