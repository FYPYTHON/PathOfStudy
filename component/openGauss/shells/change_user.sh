#!/bin/bash

password=`echo "c3NzCg=="|base64 -d`
user=test
gsql -r -d postgres -p 5433 -U omm -W $password -c "create user $user with createdb opradmin sysadmin password '$password';alter user $user with createdb opradmin sysadmin"

