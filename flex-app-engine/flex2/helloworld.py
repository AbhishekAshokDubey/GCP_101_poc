def app(environ, start_response):
    import numpy as np
    import pandas as pd
    """Simplest possible application object"""
    data = 'Hello, numpy !\n'
    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])