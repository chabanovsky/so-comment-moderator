import os
import sys

sys.path.append('/home/')
sys.path.append('/home/comment_moderator')

def application(environ, start_response):
    from comment_moderator.moderator import app as _application
    return _application(environ, start_response)

