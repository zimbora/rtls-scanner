import os

class configuration:

    def __init__ (self):
        self.localhost      = os.environ.get('localhost') or "localhost"
        self.web_port       = os.environ.get('web_port') or 80
        self.domain         = os.environ.get('domain') or "https://my.dev.inloc.cloud/api";
        self.token          = os.environ.get('token') or ""
