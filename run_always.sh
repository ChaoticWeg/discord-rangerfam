#!/bin/bash

# shoutout to SE user speakr - https://superuser.com/users/138199/speakr
# taken from https://superuser.com/a/461560

until main.py; do
    echo "wegbot crashed with exit code $?. Restarting..." >&2
    sleep 1
done
