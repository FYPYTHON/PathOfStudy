# coding=utf-8
from handlers.hd_image import ImageHandler
from tornado.web import StaticFileHandler
path_regex = r"(?P<path>(?:(?:/[^/]+)+|/?))"
url = [                            #
    (r"/matimage", ImageHandler),
]
