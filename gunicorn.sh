#!/bin/bash
gunicorn todo_app.app:app --preload -b 0.0.0.0:80