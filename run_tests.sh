#!/bin/sh

export ZEEGUU_WEB_CONFIG=`pwd`/default_web.cfg
export PYTHONWARNINGS='ignore'
python -m pytest --version 1>/dev/null 2>/dev/null || (echo "installing pytest..." && pip install pytest) && python -m pytest
export PYTHONWARNINGS='default'
