#!/bin/bash
export DYLD_LIBRARY_PATH=/opt/local/lib:$DYLD_LIBRARY_PATH
poetry run python manage.py runserver 