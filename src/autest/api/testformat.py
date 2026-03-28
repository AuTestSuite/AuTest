import autest.glb as glb
import hosts.output as host


def RegisterTestFormat(load, typename, ext=None):
    '''
    Registers a custom test loader based on a filename suffix.

    The loader will be called with the Test object when a matching file is
    discovered. More-specific suffixes win over less-specific suffixes.
    '''
    if not glb.running_main:
        return

    if not callable(load):
        host.WriteError("Custom test format loader must be callable")

    glb.TestFormatMap[typename] = load
    for e in ext or []:
        glb.TestExtMap[e] = load
