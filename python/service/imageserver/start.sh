#!/bin/bash

find /opt/midware/imageserver/lib  -type d -name __pycache__ | xargs rm -rf
# PYTHONPATH=/opt/midware/FSTornado/python3_baselib/lib/python3.5/site-packages:/opt/midware/FSTornado/python3_fs/lib/python3.5/site-packages
PYTHONPATH=/opt/midware/imageserver/lib/lib/python3.8/site-packages /opt/midware/python3.8/bin/python3 /opt/midware/imageserver/imageserver_app.py & > /dev/null 2>&1
