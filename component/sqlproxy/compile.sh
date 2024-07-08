#!/bin/bash

export GO111MODULE=on
#go mod tidy
#go mod vendor

go build -mod vendor -o sqlproxy
