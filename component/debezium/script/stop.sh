#!/bin/bash

ps -ef | grep "postgres" | grep "pgsql" | grep -v grep | awk '{print $2}' | xargs kill -9
