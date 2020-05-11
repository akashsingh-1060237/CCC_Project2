#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -vvv -i hosts --ask-become-pass all-in-one.yaml