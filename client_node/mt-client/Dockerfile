FROM node:14 as build

# Copies package.json and package-lock.json to Docker environment
COPY package*.json ./

ENV PORT=3000

# Installs all node packages
RUN rm -rf node_modules
RUN npm install
RUN npm install --save-dev

# Copies everything over to Docker environment
COPY . .

# Uses port which is used by the actual application
EXPOSE 80

# ------------------------------------------------------------

FROM nginx:1.12-alpine AS server

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

# -----------------------------------------------------------

FROM node:14 as build-prod

COPY --from=build ./ ./

# Finally runs the application
RUN npm run build:prod

# Creates production environment
FROM server AS prod

COPY --from=build-prod ./build /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
