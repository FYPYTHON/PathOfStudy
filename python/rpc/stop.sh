#!/bin/bash

netstat -ntlp | grep 9251 | awk '{print $7}' | tr "/" " " | awk '{print $1}' | xargs kill -9

