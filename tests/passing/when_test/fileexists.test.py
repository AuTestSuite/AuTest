import os

Test.Summary = "Test file modification logic"

f1 = Test.Disk.File('file-mod-1', exists=True)
fpath1 = f1.AbsPath

f2 = Test.Disk.File('file-mod-2', exists=True)

filename = 'file-mod-3'

f3 = Test.Disk.File(filename, exists=True)

Setup.Copy("utils/filemod.py", "filemod")
Setup.Copy("utils/filecat.py", "read")

# file object
tr = Test.AddTestRun()
tr.Processes.Process("writer", "python filemod {0} 1 ".format(fpath1))
tr.Command = "python read {}".format(fpath1)
tr.Processes.Default.StartBefore(
    tr.Processes.writer, ready=When.FileExists(f1))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer2", "python filemod {0} 1 ".format(f2.AbsPath))
tr.Command = "python read {}".format(f2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer2, ready=When.FileExists(f2.AbsPath))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer3", "python filemod {0} 1 ".format(filename))
tr.Command = "python read {}".format(filename)
tr.Processes.Default.StartBefore(
    tr.Processes.writer3, ready=When.FileExists(filename))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")
