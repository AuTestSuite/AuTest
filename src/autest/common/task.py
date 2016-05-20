from __future__ import absolute_import, division, print_function

class Task(object):
    def __init__(self, callback):
        self.__func=callback

    def run(self):
        host.VerboseMessage(['task'],"Starting Task")
        try:
            ret=self.__func()
        except KeyboardInterrupt:
            raise
        except:
            # something went wrong...
            ret=1
        host.VerboseMessage(['task'],"Task Finished")
        return ret
