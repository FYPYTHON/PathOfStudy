#!/bin/bash


kill -9 `ps -ef | grep java | grep jenkins | awk {'print $2'}`



