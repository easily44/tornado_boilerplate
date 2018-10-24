import os


LOG_DIR = '/var/log/api'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s - %(module)s|%(funcName)s|'
                      '%(lineno)d: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'uncaught': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_DIR + '/error.log',
            'when': 'midnight',
            'backupCount': 90,
            'formatter': 'simple',
        },
        'error': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_DIR + '/error.log',
            'when': 'midnight',
            'backupCount': 90,
            'formatter': 'default',
        }
    },
    'loggers': {
        'tornado.application': {
            'handlers': ['uncaught'],
            'propagate': True,
        },
        'tornado.general': {
            'handlers': ['error'],
            'propagate': True,
        }
    }
}