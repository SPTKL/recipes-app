#!/bin/bash
gunicorn app:server --bind=:5000 --workers=3 --threads=3
# python3 app.py