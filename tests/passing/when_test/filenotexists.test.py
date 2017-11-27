import os

Test.Summary = "Test file modification logic"

f1 = Test.Disk.File('file-mod-1', exists=False)
fpath1 = f1.AbsPath

f2 = Test.Disk.File('file-mod-2', exists=False)

filename = 'file-mod-3'

f3 = Test.Disk.File(filename, exists=False)

f1.WriteOn('heyyy')
f2.WriteOn('heyyy')
f3.WriteOn('heyyy')

Setup.Copy("utils/filedel.py", "filedel")

# file object
tr = Test.AddTestRun()
tr.Processes.Process("writer", "python filedel {0} 1 ".format(fpath1))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(fpath1)
tr.Processes.Default.StartBefore(
    tr.Processes.writer, ready=When.FileNotExists(f1))

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer2", "python filedel {0} 1 ".format(f2.AbsPath))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(f2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer2, ready=When.FileNotExists(f2.AbsPath))

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer3", "python filedel {0} 1 ".format(filename))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(filename)
tr.Processes.Default.StartBefore(
    tr.Processes.writer3, ready=When.FileNotExists(filename))
