"""Configuration from environment only. Never log credential values."""
import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', '5432'))
if not 1 <= DB_PORT <= 65535:
    raise ValueError('DB_PORT must be between 1 and 65535')

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
GITHUB_PAT_TOKEN = os.environ.get('GITHUB_PAT_TOKEN')
