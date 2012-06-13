#!/bin/sh

cat nagext.tmpl.py > nagext/commands.py

./nagext/importer.py >> nagext/commands.py
