from os.path import getmtime
from os import getcwd

from autest.api import AddWhenFunction
from autest.testenities.file import File
import hosts.output as host

def FileModified(file_input):
    file_path = file_input.AbsPath if isinstance(
        file_input, File) else file_input
    state = {}

    def file_is_modified():
        host.WriteDebug(
            ['file', 'when'],
            "working out of directory {0}".format(getcwd())
        )
        current_mtime = getmtime(file_path)

        if "modify_time" in state:
            host.WriteDebug(["file", "when"],
                            "file was last modified at {0}".format(state["modify_time"]))
            return state["modify_time"] < current_mtime

        state["modify_time"] = current_mtime
        return False

    return file_is_modified


AddWhenFunction(FileModified, generator=True)
