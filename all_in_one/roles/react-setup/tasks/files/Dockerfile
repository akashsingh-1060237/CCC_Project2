FROM node:12 AS builder
WORKDIR /app
COPY . .
RUN yarn run build


FROM node:12
RUN yarn config set proxy http://wwwproxy.unimelb.edu.au:8000
RUN yarn config set https-proxy http://wwwproxy.unimelb.edu.au:8000
RUN yarn global add serve
WORKDIR /app
COPY --from=builder /app/build .
CMD ["serve", "-p", "3000", "-s", "."]