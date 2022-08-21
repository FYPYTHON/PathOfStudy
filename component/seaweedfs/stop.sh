#!/bin/bash


ps -ef | grep "weed" | grep -v grep | awk '{print $2}' | xargs kill -9
