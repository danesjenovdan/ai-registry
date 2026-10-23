FROM node:26-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY .browserslistrc ./

CMD ["npm", "run", "build"]
