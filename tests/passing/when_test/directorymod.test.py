Test.Summary = "Test Directory modification logic"

d1 = Test.Disk.Directory('directory-mod-1', exists=True)
directory_path_1 = d1.AbsPath

d2 = Test.Disk.Directory('directory-mod-2', exists=True)

relative_directory_path = 'directory-mod-3'
d3 = Test.Disk.Directory(relative_directory_path, exists=True)

Setup.Copy("utils/directorymod.py", "directorymod")
Setup.Copy("utils/directorylist.py", "read")

# Directory object
tr = Test.AddTestRun()
tr.Processes.Process("writer", "python directorymod {0} 2 ".format(directory_path_1))
tr.Command = "python read {}".format(directory_path_1)
# Note that d1 is a Test.Disk.Directory object
tr.Processes.Default.StartBefore(
    tr.Processes.writer, ready=When.DirectoryModified(d1))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "first_file", "Did the directory really get created?")

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer2", "python directorymod {0} 2 ".format(d2.AbsPath))
tr.Command = "python read {}".format(d2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer2, ready=When.DirectoryModified(d2.AbsPath))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "first_file", "Did the directory really get created?")

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer3", "python directorymod {0} 2 ".format(relative_directory_path))
tr.Command = "python read {}".format(relative_directory_path)
tr.Processes.Default.StartBefore(
    tr.Processes.writer3, ready=When.DirectoryModified(relative_directory_path))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "first_file", "Did the directory really get created?")

#
# The below are the same as above, but uses the DirModified shortcut.
#

d1 = Test.Disk.Directory('dir-mod-1', exists=True)
directory_path_1 = d1.AbsPath

d2 = Test.Disk.Directory('dir-mod-2', exists=True)

relative_directory_path = 'dir-mod-3'
d3 = Test.Disk.Directory(relative_directory_path, exists=True)

# Directory object
tr = Test.AddTestRun()
tr.Processes.Process("writer4", "python directorymod {0} 2 ".format(directory_path_1))
tr.Command = "python read {}".format(directory_path_1)
# Note that d1 is a Test.Disk.Directory object
tr.Processes.Default.StartBefore(
    tr.Processes.writer4, ready=When.DirModified(d1))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "first_file", "Did the directory really get created?")

# absolute path
tr = Test.AddTestRun()
tr.Processes.Process("writer5", "python directorymod {0} 2 ".format(d2.AbsPath))
tr.Command = "python read {}".format(d2.AbsPath)
tr.Processes.Default.StartBefore(
    tr.Processes.writer5, ready=When.DirModified(d2.AbsPath))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "first_file", "Did the directory really get created?")

# relative path
tr = Test.AddTestRun()
tr.Processes.Process("writer6", "python directorymod {0} 2 ".format(relative_directory_path))
tr.Command = "python read {}".format(relative_directory_path)
tr.Processes.Default.StartBefore(
    tr.Processes.writer6, ready=When.DirModified(relative_directory_path))
tr.Processes.Default.Streams.stdout = Testers.ContainsExpression(
    "first_file", "Did the directory really get created?")
