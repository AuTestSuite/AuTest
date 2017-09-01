import os

Test.Summary = "Test file modification logic"

f1 = Test.Disk.File('my_great_file', exists=False)
fpath1 = f1.AbsPath

f2 = Test.Disk.File('my_spectacular_file', exists=False)

filename = 'my_fantastic_file'

f3 = Test.Disk.File(filename, exists=False)

Setup.Copy("utils/filemod.py", "mod")
Setup.Copy("utils/filecat.py", "read")
f1.WriteOn('heyyy')
f2.WriteOn('heyyy')
f3.WriteOn('heyyy')

# file object
tr = Test.AddTestRun()
tr.Processes.Process("writer", "python mod {0} 2 ".format(fpath1))
tr.Command = "python read {}".format(fpath1)
tr.Processes.Default.StartBefore(
    tr.Processes.writer, ready=When.FileModified(f1))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer2", "python mod {0} 3 ".format(f2.AbsPath))
tr.Command = "python read {}".format(f2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer2, ready=When.FileModified(f2.AbsPath))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer3", "python mod {0} 4 ".format(filename))
tr.Command = "python read {}".format(filename)
tr.Processes.Default.StartBefore(
    tr.Processes.writer3, ready=When.FileModified(filename))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")
