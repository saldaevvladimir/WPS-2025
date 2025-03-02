FROM node:alpine3.21

WORKDIR /REACT_APP

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview"]