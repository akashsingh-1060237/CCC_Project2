FROM node:12
WORKDIR /app
COPY . .
RUN yarn config set proxy http://wwwproxy.unimelb.edu.au:8000
RUN yarn config set https-proxy http://wwwproxy.unimelb.edu.au:8000
RUN yarn install
CMD yarn start