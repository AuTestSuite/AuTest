import os


Test.Summary = '''
Test the execution of a Process cleanup function.
'''

t = Test.AddTestRun("Test execution of cleanup of a Process")

cleanup_file = os.path.join(t.RunDirectory, "cleanup_file")

t.Disk.File(cleanup_file, id="cleanup_file", exists=True)

t.Processes.Default.Command = "echo 'Just echoing something'"
t.Processes.Default.ReturnCode = 0
t.Processes.Default.Setup.Lambda(
    func_cleanup=lambda: open(cleanup_file, "wt").write("Doing some cleanup.\n"),
    description="Printing in cleanup function")

t.Disk.cleanup_file.Content = Testers.ContainsExpression(
    "Doing some cleanup.",
    "The cleanup function should have been called.")
