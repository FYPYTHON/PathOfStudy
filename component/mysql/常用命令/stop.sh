#!/bin/bash

ps -ef | grep mysql | grep -v "grep" | awk '{print $2}' | xargs kill -9




