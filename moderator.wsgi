import os
import sys

sys.path.append('/home/')
sys.path.append('/home/benice')

def application(environ, start_response):
    from benice.moderator import app as _application
    return _application(environ, start_response)

