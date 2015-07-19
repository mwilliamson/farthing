#!/usr/bin/env sh

make bootstrap
. _virtualenv/bin/activate
farthing demo/fact.py _virtualenv/bin/nosetests demo/tests.py
