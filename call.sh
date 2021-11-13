#!/bin/bash

TryDumbBot () {
    python3 dumbbot.py
}

n=0

while true; do
    if ! TryDumbBot ; then
        n=$[$n+1]
    fi

    if [ "$n" = "10" ]; then
        sleep 60
        n=0
    fi
done
