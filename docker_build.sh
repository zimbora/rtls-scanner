#!/bin/bash
VERSION=0.4.0
#local
#docker build --force-rm -t rtls-controller:$VERSION -f Dockerfile .

# remote repo
# armv7 version
docker buildx build --force-rm --push --platform linux/arm/v7 -t zimbora/rtls-scanner-armv7:$VERSION -t zimbora/rtls-scanner-armv7:latest -f Dockerfile .
# amd64 version
#docker buildx build --force-rm --platform linux/amd64 -t zimbora/rtls-scanner-amd64:$VERSION -t zimbora/rtls-scanner-amd64:latest -f Dockerfile .
