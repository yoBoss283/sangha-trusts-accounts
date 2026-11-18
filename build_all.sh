#!/bin/sh
# Rebuild every report page from its saved data, then the landing page (index.html, pages/, and each folder's index.html).
# To rebuild a monastery from its source documents (PDFs), run that folder's own build.sh first.
set -e
cd "$(dirname "$0")"
for d in est aruna-ratanagiri hartridge sumedharama; do (cd "$d" && python3 build.py); done
python3 simple_build.py
python3 build.py
