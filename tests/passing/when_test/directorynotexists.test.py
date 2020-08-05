Test.Summary = "Test Directory non-existence logic"

d1 = Test.Disk.Directory('directory-not-exists-1', exists=False)
dpath1 = d1.AbsPath

d2 = Test.Disk.Directory('directory-not-exists-2', exists=False)

relative_directory_path = 'directory-not-exists-3'

f3 = Test.Disk.Directory(relative_directory_path, exists=False)

Setup.Copy("utils/directorydel.py", "directorydel")

# Directory object
tr = Test.AddTestRun()
tr.Processes.Process("writer", "python directorydel {0} 1 ".format(dpath1))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(dpath1)
# Note that d1 is a Test.Disk.Directory object
tr.Processes.Default.StartBefore(
    tr.Processes.writer, ready=When.DirectoryNotExists(d1))

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer2", "python directorydel {0} 1 ".format(d2.AbsPath))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(d2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer2, ready=When.DirectoryNotExists(d2.AbsPath))

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer3", "python directorydel {0} 1 ".format(relative_directory_path))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(relative_directory_path)
tr.Processes.Default.StartBefore(
    tr.Processes.writer3, ready=When.DirectoryNotExists(relative_directory_path))

#
# The below are the same as above, but uses the DirNotExists shortcut.
#

d1 = Test.Disk.Directory('dir-not-exists-1', exists=False)
dpath1 = d1.AbsPath

d2 = Test.Disk.Directory('dir-not-exists-2', exists=False)

relative_directory_path = 'dir-not-exists-3'

f3 = Test.Disk.Directory(relative_directory_path, exists=False)

# Directory object
tr = Test.AddTestRun()
tr.Processes.Process("writer4", "python directorydel {0} 1 ".format(dpath1))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(dpath1)
# Note that d1 is a Test.Disk.Directory object
tr.Processes.Default.StartBefore(
    tr.Processes.writer4, ready=When.DirNotExists(d1))

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer5", "python directorydel {0} 1 ".format(d2.AbsPath))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(d2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer5, ready=When.DirNotExists(d2.AbsPath))

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer6", "python directorydel {0} 1 ".format(relative_directory_path))
tr.Command = "python -c \"import os; os.path.exists('{}')\"".format(relative_directory_path)
tr.Processes.Default.StartBefore(
    tr.Processes.writer6, ready=When.DirNotExists(relative_directory_path))
