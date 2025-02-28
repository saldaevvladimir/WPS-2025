FROM node:alpine3.21

WORKDIR /REACT_APP

COPY package*.json .

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
# поменять на npm run preview потом