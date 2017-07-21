#! pylti config file

import os

WTF_CSRF_ENABLED = True

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "you-will-never-guess")

PYLTI_CONFIG = {
    'consumers': {
        'hello': {
            'secret': 'hello_secret1970'
        },
    }
}
