#!/usr/bin/env bash

crontab -l > tempfile
echo "0 8,18 * * 1-5 `readlink -f run.sh`" >> tempfile
crontab tempfile
rm tempfile
