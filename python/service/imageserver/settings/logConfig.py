# coding=utf-8
logConfig = {

    'version': 1,
    'loggers': {
      'root': {
        'level': 'INFO',
        'handlers': ['access']
      },
      'tornado.access': {
        'level': 'INFO',
        'handlers': ['access'],
        'propagate': 'no'
      },
      'tornado.application': {
        'level': 'INFO',
        'handlers': ['log'],
        'propagate': 'no'
      }
    },
    'formatters': {
      'simple': {
        # 'format': '[%(levelname)s] %(name)s %(funcName)s %(asctime)s %(filename)s %(lineno)s:%(message)s'
        'format': '%(levelname)s %(asctime)s %(filename)15s %(lineno)s:%(message)s'
      },
      'timedRotating': {
        'format': '%(levelname)s %(asctime)s %(filename)15s [%(lineno)s] - %(message)s'
      }
    },
    'handlers': {
      'access': {
        'class': 'logging.handlers.TimedRotatingFileHandler',  # time
        'level': 'INFO',
        'formatter': 'simple',
        'filename': '/opt/log/fs/imageserver_access.log',
        'when': 'midnight',
        'interval': 1,
        'backupCount': 2,    # u"备份数"
        'encoding': 'utf8'
        },
      'log': {
        'class': 'logging.handlers.RotatingFileHandler',    # size
        'level': 'INFO',
        'formatter': 'timedRotating',
        'filename': '/opt/log/fs/imageserver.log',
        # 'when': 'midnight',
        # 'interval': 1,
        'backupCount': 2,    # 日志文件的保留个数
        'maxBytes': 50 * 1024 * 1024,  # 文件最大50M
        'encoding': 'utf-8'
        }
    }
}
