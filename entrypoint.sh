#!/bin/bash
gunicorn app:app --bind=:$PORT --workers=5 --threads=3
# python3 app.py