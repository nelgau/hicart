#!/bin/bash
set -eufo pipefail

OS=`uname -s`

if [ "${OS}" == "Darwin" ]; then
    open -a ares $1
else
    echo "Error: Launching in ares is unsupported on ${OS}."
fi
