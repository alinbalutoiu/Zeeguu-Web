#!/bin/sh

export ZEEGUU_WEB_CONFIG=`pwd`/default_web.cfg
export PYTHONWARNINGS='ignore'
python3.6 -m pytest --version 1>/dev/null 2>/dev/null || (echo "installing pytest..." && pip3.6 install pytest) && python3.6 -m pytest
export PYTHONWARNINGS='default'
