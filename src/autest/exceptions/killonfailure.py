from __future__ import absolute_import, division, print_function

class KillOnFailureError(Exception):
    def __init__(self, message=None, **kwargs):
        self.info=message
        return super().__init__(message,**kwargs)