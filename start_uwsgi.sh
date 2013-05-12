#!/usr/bin/env sh

mkdir -p cache
uwsgi_python -s /tmp/uwsgi_partmon.sock -w partmom:app --processes 4 -C a+rw
