#!/bin/bash

# shoutout to SE user speakr - https://superuser.com/users/138199/speakr
# taken from https://superuser.com/a/461560

thisdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pyfile="${thisdir}/main.py"

until python "${pyfile}"; do
    echo "wegbot crashed with exit code $?. Restarting..." >&2
    sleep 1
done

