#!/bin/bash

# kill existing processes with extreme prejudice
pkill -f discord-rangerfam

# some setup
export thisdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export runalways="${thisdir}/run_always.sh"
export logfile="${thisdir}/run.log"

# run run_always in the background, ignoring sighup
nohup bash "${runalways}" >"${logfile}" 2>&1 &

