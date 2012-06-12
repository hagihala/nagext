#!/bin/sh

cat nagext.tmpl.py > nagext.py

./nagext/importer.py >> nagext.py
