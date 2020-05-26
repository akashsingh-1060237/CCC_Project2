#!/usr/bin/env sh

# Replace the substring with the value of the environment variable ${WELCOME_STRING}

sudo sed -i 's/Welcome to nginx!/Welcome to '"${WELCOME_STRING}"'!/g' /usr/share/nginx/html/index.html

# Make the entrypoint a pass through, then runs the docker command
sudo exec "$@"



