# This script is to used for development purpose only.


#!/bin/bash
export FLASK_APP=./src/app.py
export FLASK_ENV=development

flask run --port 5000
