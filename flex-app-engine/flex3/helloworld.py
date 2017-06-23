import logging
import webapp2
from subprocess import Popen, PIPE
import numpy as np

class OkHandler (webapp2.RequestHandler):
    def get (self): 
        self.response.write ('ok')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        domain = self.request.get ('domain')
        cmd = ["gwhois", domain]
        process = Popen (cmd, stdout=PIPE, stderr=PIPE)
        output, err = process.communicate()
        exit_code = process.wait()
        self.response.write('stdout: %s' % output)
        logging.info ('stderr: %s' % err)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/_ah/start', OkHandler),
    ('/_ah/health', OkHandler)
], debug=True)