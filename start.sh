#!/bin/bash

thisdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
runalways="${thisdir}/run_always.sh"
logfile="${thisdir}/run.log"

nohup bash "${runalways}" >"${logfile}" 2>&1 &

