import os

from api.app import app

app.debug = os.environ.get('DEBUG') in ('True', 'TRUE')
