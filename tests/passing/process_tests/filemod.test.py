import os

Test.Summary = "Test file modification logic"

filename = 'my_great_file'
f = Test.Disk.File(filename, exists=False)
fpath = f.AbsPath

Setup.Copy("filemod.py", "mod")
Setup.Copy("filecat.py", "read")
f.WriteOn('heyyy')


tr = Test.AddTestRun()
tr.Processes.Process("writer", "python mod {} 2 ".format(fpath))
tr.Command = "python read {}".format(fpath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer, ready=When.FileModified(f))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "caught at the right time", "Did the file really change?")
