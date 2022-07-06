#!/bin/bash
poetry run gunicorn -b 0.0.0.0:80 -w 2 todo_app.app:app
