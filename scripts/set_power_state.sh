#!/usr/bin/env bash
set -eufo pipefail

state=""
silent=""

while [[ $# -gt 0 ]] ; do
  case $1 in
    -n|--state)
      state="$2"
      shift
      shift
      ;;
    -l|--silent)
      silent=true
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      echo "Syntax error at $1"
      exit 1
      ;;
  esac
done

if [[ -z ${IBOOT_G2_HOSTNAME:-} ]] ; then
    if [[ -z $silent ]] ; then
        echo "No hostname given. Please set IBOOT_G2_HOSTNAME env var."
        exit 1
    else
        exit 0
    fi
fi

if [[ -z $state ]] ; then
    echo "No state given. Please provide --state argument."
    exit 1
fi

curl -sS "http://${IBOOT_G2_HOSTNAME}/?s=${state}" > /dev/null
