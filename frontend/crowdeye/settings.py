import logging
# This logging system is based off one from the django documentation: https://docs.djangoproject.com/en/3.1/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    
    'handlers': {
        'file_log_all': { # To log everything
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple' # The info message shouldn't have errors so its fine to be simple
            'filename' : 'logs/info_log.log'
            'maxBytes' : 1024*1024*5 # 5MB
        },
        'file_log_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple' # The info message shouldn't have errors so its fine to be simple
            'filename' : 'logs/info_log.log'
            'maxBytes' : 1024*1024*5 # 5MB
        },
        'file_log_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose' # The error messages are important to understand and should therefore have metadata
            'filename' : 'logs/error_log.log'
            'maxBytes' : 1024*1024*5 # 5MB
        }
        'file_log_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose' # The debug messages are important to understand and should therefore have metadata
            'filename' : 'logs/debug_log.log'
            'maxBytes' : 1024*1024*5 # 5MB
        }
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'file': {
            'handlers': ['file_log_all'],
            'level': 'INFO',
            'propagate' : False
        },
        'file.info': {
            'handlers': ['file_log_info'],
            'level': 'ERROR',
            'propagate' : False
        },
        'file.error': {
            'handlers': ['file_log_error'],
            'level': 'ERROR',
            'propagate' : True
        },
        'file.debug': {
            'handlers': ['file_log_debug'],
            'level': 'DEBUG',
            'propagate' : False
        }
    }
}