FROM node:18
ENV NODE_ENV=production

RUN apt-get update || : && apt-get install python -y || : && apt-get install chromium -y 

WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install

COPY . .

CMD [ "node", "index.js" ]
